from __future__ import annotations

import fnmatch
from dataclasses import dataclass


@dataclass(frozen=True)
class ScopeDecision:
    allowed: bool
    path: str
    reason: str


def check_path(path: str, allow: list[str], deny: list[str]) -> ScopeDecision:
    path = path.replace("\\", "/")
    if any(fnmatch.fnmatch(path, pat) for pat in deny):
        return ScopeDecision(False, path, "matched deny rule")
    if allow and not any(fnmatch.fnmatch(path, pat) for pat in allow):
        return ScopeDecision(False, path, "outside allow rules")
    return ScopeDecision(True, path, "allowed")


def check_paths(paths: list[str], allow: list[str], deny: list[str]) -> list[ScopeDecision]:
    return [check_path(p, allow, deny) for p in paths]
