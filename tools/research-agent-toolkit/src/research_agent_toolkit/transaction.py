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
    """Fail closed: arbitrary Python callback writes cannot be file-confined.

    This legacy method does not run `mutate`, `verifier`, or filesystem
    operations. Snapshotting listed paths cannot control undeclared writes,
    symlink escapes, callback exceptions, or verifier spawn failures.

    Authorized research patches must instead use the separately approved,
    provenance-scoped mutation service in an explicitly disposable worktree.
    No claim of operating-system sandboxing is made for that service.
    """
    raise PermissionError(
        "verified_mutation is disabled: unrestricted callbacks cannot be "
        "confined or rolled back; use approved governed_patch_mutation "
        "in an isolated disposable worktree"
    )


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
