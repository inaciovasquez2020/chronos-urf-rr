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
    """Broad destructive recovery is forbidden. This method never mutates Git."""
    raise RuntimeError(
        "unsafe repository-wide rollback disabled; use exact-file recovery in "
        "an approved disposable worktree"
    )


def verified_dependency_subprocess(
    root: str | Path,
    closure: list[str],
    mutation: list[str],
    verifier: list[str],
) -> DependencyTransactionResult:
    """Legacy arbitrary subprocess writes are disabled, including direct callers.

    Go through `governed_patch_mutation` with versioned policy, an exact
    provenance closure, and scoped signed approval. Never silently fall back
    to `git reset --hard` or `git clean -fd`.
    """
    return DependencyTransactionResult(
        False,
        "LEGACY_MUTATION_DISABLED",
        2,
        (),
        tuple(sorted(closure)),
        "",
        "trusted signed approval and disposable worktree are required",
    )
