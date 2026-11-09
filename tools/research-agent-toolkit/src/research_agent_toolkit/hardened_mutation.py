"""Fail-closed replacement for the old `rat mutate` implementation.

This module is deliberately not auto-activated by importing it. Its caller must
supply versioned policy plus a separately authorized, scoped MAC. All writes
remain in an explicitly disposable Git worktree. No reset/clean operations.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .budgets import Budget, BudgetExceeded
from .engine import evaluate
from .provenance import build_provenance, forward_closure, load_manifest
from .lean_exact import exact_lean_dependencies
from .transaction import DependencyTransactionResult


def _guard():
    # The guarded adapter added in PR #1338 is intentionally a required
    # dependency; its absence must deny writes, not enable legacy fallback.
    ai = Path(__file__).resolve().parents[2] / "urf-ai"
    if not (ai / "urf_ai" / "guard.py").is_file():
        raise RuntimeError("required URF-AI guarded mutation dependency missing")
    if str(ai) not in sys.path:
        sys.path.insert(0, str(ai))
    from urf_ai.guard import patch_paths, run_mutation
    return patch_paths, run_mutation


def governed_patch_mutation(
    root: str | Path,
    manifest: str | Path,
    changed: str,
    patch: str,
    verifier: list[str],
    *,
    modules: list[str] | None = None,
    config_path: str | Path | None = None,
    approval: dict | None = None,
    authorization_key: bytes | None = None,
    timeout_seconds: int = 10,
    approval_ledger: str | Path | None = None,
) -> DependencyTransactionResult:
    """Deny unapproved mutations; stage verified patches in disposable roots only.

    A verified candidate is NOT committed or promoted. A signature binding the
    exact root, HEAD, patch, closure, config and verifier must come from a
    distinct trusted authorization controller, never the research agent.
    """
    root = Path(root).resolve(strict=True)

    def denial(phase: str, reason: str, code: int = 2):
        return DependencyTransactionResult(
            False, phase, code, (), (), "", reason,
        )

    if approval_ledger is None:
        return denial("authorization", "trusted durable approval ledger required")
    if config_path is None or approval is None or authorization_key is None:
        return denial("authorization", "explicit config and scoped approval required")
    if not isinstance(patch, str) or not patch.strip():
        return denial("preflight", "empty patch")
    if not isinstance(changed, str) or not changed:
        return denial("preflight", "empty provenance node")
    if not isinstance(verifier, list) or not verifier or not all(
        isinstance(v, str) and v for v in verifier
    ):
        return denial("preflight", "verifier argv must be nonempty list of strings")

    # Never accept a config file outside this particular disposable repo.
    config_candidate = (root / config_path) if not Path(config_path).is_absolute() else Path(config_path)
    if config_candidate.is_symlink():
        return denial("policy", "policy config symlink is prohibited")
    cfgfile = config_candidate.resolve()
    try:
        cfgfile.relative_to(root)
    except ValueError:
        return denial("policy", "policy config escapes repository")
    if not cfgfile.is_file() or cfgfile.is_symlink():
        return denial("policy", "policy config must be an ordinary repository file")
    try:
        config = json.loads(cfgfile.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return denial("policy", f"unreadable policy: {exc}")
    if not isinstance(config, dict):
        return denial("policy", "policy must be a JSON object")

    manifest_candidate = (root / manifest) if not Path(manifest).is_absolute() else Path(manifest)
    if manifest_candidate.is_symlink():
        return denial("provenance", "provenance manifest symlink is prohibited")
    mf = manifest_candidate.resolve()
    try:
        mf.relative_to(root)
    except ValueError:
        return denial("provenance", "manifest escapes repository")
    if not mf.is_file() or mf.is_symlink():
        return denial("provenance", "provenance manifest missing or symlinked")
    try:
        graph = build_provenance(
            root,
            load_manifest(mf),
            exact_lean_dependencies(root, modules) if modules else None,
        )
        ids = {n.id for n in graph.nodes}
        normalized = changed.replace("\\", "/")
        if normalized not in ids:
            return denial("provenance", "changed node absent from provenance graph")
        reachable = forward_closure(graph, [normalized])
        closure = {n.id.replace("\\", "/") for n in graph.nodes
                   if n.kind in {"generator", "artifact", "test"}
                   and n.id.replace("\\", "/") in reachable}
        if not closure:
            return denial("provenance", "provenance closure contains no mutable files")
        patch_paths, run_mutation = _guard()
        paths = patch_paths(root, patch.encode("utf-8"))
    except (RuntimeError, ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        return denial("preflight", repr(exc))
    if not paths or not paths <= closure:
        return denial("closure", "patch paths escape exact provenance closure", 3)

    # Invoke the same scope/policy/gate/budget engine as `rat gate` on the
    # *actual patch paths and added source*, not merely on a caller's label.
    added = "\n".join(
        l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++")
    )
    try:
        decision = evaluate(config, "modify", sorted(paths), added,
                            Budget(config.get("budgets", {})))
    except (BudgetExceeded, ValueError, KeyError, TypeError) as exc:
        return denial("policy", repr(exc))
    if decision.status != "VERIFY":
        return denial("policy", "mutation requires explicit VERIFY policy gate: " + "; ".join(decision.reasons))

    result = run_mutation(
        root, patch.encode("utf-8"), closure, config, verifier,
        approval=approval, authorization_key=authorization_key,
        timeout_seconds=timeout_seconds,
        approval_ledger=approval_ledger,
    )
    # Successful internal diff/syntax checks STAGE a candidate; they cannot
    # certify research claims. The legacy result schema must not expose that
    # staging operation as preserved=True or a zero verification return code.
    staged = result.status == "STRUCTURAL_CANDIDATE_NOT_PROMOTED"
    return DependencyTransactionResult(
        preserved=False,
        phase="STRUCTURAL_STAGED_UNVERIFIED" if staged else result.stage,
        returncode=4 if staged else (result.returncode or 2),
        changed_paths=tuple(sorted(paths)) if staged else result.residue,
        closure=tuple(sorted(closure)),
        stdout=result.status,
        stderr=("Patch remains staged in the disposable worktree; "
                "NO mathematical/theorem verification was performed. "
                + result.detail) if staged else result.detail,
    )
