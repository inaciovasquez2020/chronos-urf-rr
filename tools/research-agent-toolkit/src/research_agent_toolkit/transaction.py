from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class VerificationResult:
    preserved: bool
    returncode: int
    stdout: str
    stderr: str


def verified_mutation(
    paths: list[str | Path],
    mutate: Callable[[], None],
    verifier: list[str],
    cwd: str | Path | None = None,
) -> VerificationResult:
    """Apply one mutation, verify immediately, and exactly restore touched files on failure.

    Only listed files are snapshotted/restored. Creation/deletion of listed paths is handled.
    The caller is responsible for ensuring the mutation does not touch unlisted paths.
    """
    targets = [Path(p) for p in paths]
    snapshots: dict[Path, bytes | None] = {
        p: p.read_bytes() if p.exists() else None for p in targets
    }
    mutate()
    proc = subprocess.run(verifier, cwd=cwd, text=True, capture_output=True)
    if proc.returncode == 0:
        return VerificationResult(True, 0, proc.stdout, proc.stderr)

    for path, data in snapshots.items():
        if data is None:
            if path.exists():
                path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return VerificationResult(False, proc.returncode, proc.stdout, proc.stderr)


@dataclass(frozen=True)
class DependencyTransactionResult:
    preserved: bool
    phase: str
    returncode: int
    changed_paths: tuple[str, ...]
    closure: tuple[str, ...]
    stdout: str
    stderr: str


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)


def _changed_paths(root: Path) -> list[str]:
    proc = _git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all")
    if proc.returncode != 0:
        first = next((line for line in proc.stderr.splitlines() if line.strip()), "git status failed")
        raise RuntimeError(first)
    paths: list[str] = []
    records = [x for x in proc.stdout.split("\0") if x]
    for record in records:
        if len(record) < 4:
            continue
        path = record[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.replace("\\", "/"))
    return sorted(set(paths))


def _restore_clean_head(root: Path) -> None:
    reset = _git(root, "reset", "--hard", "HEAD")
    if reset.returncode != 0:
        first = next((line for line in reset.stderr.splitlines() if line.strip()), "git reset failed")
        raise RuntimeError(first)
    clean = _git(root, "clean", "-fd")
    if clean.returncode != 0:
        first = next((line for line in clean.stderr.splitlines() if line.strip()), "git clean failed")
        raise RuntimeError(first)


def verified_dependency_subprocess(
    root: str | Path,
    closure: list[str],
    mutation: list[str],
    verifier: list[str],
) -> DependencyTransactionResult:
    """Run one mutation in a clean Git worktree, constrain it to a dependency closure,
    verify immediately, and restore the exact clean HEAD state on the first failure.
    """
    root = Path(root).resolve()
    inside = _git(root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise RuntimeError(f"not a Git worktree: {root}")
    dirty = _changed_paths(root)
    if dirty:
        raise RuntimeError(f"working tree must be clean; first changed path: {dirty[0]}")

    allowed = {p.replace("\\", "/") for p in closure}
    mut = subprocess.run(mutation, cwd=root, text=True, capture_output=True)
    if mut.returncode != 0:
        _restore_clean_head(root)
        return DependencyTransactionResult(
            False, "mutation", mut.returncode, tuple(_changed_paths(root)), tuple(sorted(allowed)), mut.stdout, mut.stderr
        )

    changed = _changed_paths(root)
    outside = [path for path in changed if path not in allowed]
    if outside:
        _restore_clean_head(root)
        return DependencyTransactionResult(
            False,
            "closure",
            3,
            tuple(changed),
            tuple(sorted(allowed)),
            "",
            f"mutation escaped dependency closure: {outside[0]}",
        )

    check = subprocess.run(verifier, cwd=root, text=True, capture_output=True)
    if check.returncode != 0:
        _restore_clean_head(root)
        return DependencyTransactionResult(
            False, "verification", check.returncode, tuple(changed), tuple(sorted(allowed)), check.stdout, check.stderr
        )

    return DependencyTransactionResult(
        True, "verification", 0, tuple(changed), tuple(sorted(allowed)), check.stdout, check.stderr
    )
