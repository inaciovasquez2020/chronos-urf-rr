from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .lean_exact import exact_lean_dependencies
from .provenance import (
    build_provenance,
    forward_closure,
    load_manifest,
)
from .transaction import (
    DependencyTransactionResult,
    verified_dependency_subprocess,
)


_MUTABLE_PROVENANCE_KINDS = {
    "generator",
    "artifact",
    "test",
}


def _validated_command(
    command: list[str],
    label: str,
) -> list[str]:
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(item, str) and item for item in command)
    ):
        raise ValueError(
            f"{label} must be a nonempty list of nonempty strings"
        )

    return list(command)


def governed_patch_mutation(
    root: str | Path,
    manifest: str | Path,
    changed: str,
    patch: str,
    verifier: list[str],
    *,
    modules: list[str] | None = None,
) -> DependencyTransactionResult:
    """
    Apply one unified-diff mutation inside the provenance-derived
    mutable file closure, verify immediately, and restore clean HEAD
    on the first mutation, closure, or verification failure.

    This is the supported agent research-file write primitive.
    It does not install or depend on Git hooks.
    """
    root = Path(root).resolve()

    manifest_arg = Path(manifest)
    manifest_path = (
        manifest_arg.resolve()
        if manifest_arg.is_absolute()
        else (root / manifest_arg).resolve()
    )

    try:
        manifest_path.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"manifest escapes repository root: {manifest}"
        ) from exc

    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"missing provenance manifest: {manifest_path}"
        )

    if not isinstance(changed, str) or not changed:
        raise ValueError(
            "changed provenance node must be a nonempty string"
        )

    if not isinstance(patch, str) or not patch.strip():
        raise ValueError(
            "patch must be a nonempty unified diff"
        )

    verifier = _validated_command(
        verifier,
        "verifier",
    )

    requested_modules = list(modules or [])

    lean_graph = (
        exact_lean_dependencies(
            root,
            requested_modules,
        )
        if requested_modules
        else None
    )

    graph = build_provenance(
        root,
        load_manifest(manifest_path),
        lean_graph,
    )

    node_ids = {
        node.id
        for node in graph.nodes
    }

    changed = changed.replace("\\", "/")

    if changed not in node_ids:
        raise ValueError(
            "changed node is not present in provenance graph: "
            + changed
        )

    reachable = forward_closure(
        graph,
        [changed],
    )

    mutable_ids = {
        node.id.replace("\\", "/")
        for node in graph.nodes
        if node.kind in _MUTABLE_PROVENANCE_KINDS
    }

    closure = sorted(
        item.replace("\\", "/")
        for item in reachable
        if item.replace("\\", "/") in mutable_ids
    )

    if not closure:
        raise ValueError(
            "provenance closure contains no mutable repository paths"
        )

    fd, patch_name = tempfile.mkstemp(
        prefix="rat-mutate-",
        suffix=".patch",
    )
    os.close(fd)

    patch_path = Path(patch_name)

    try:
        patch_path.write_text(
            patch,
            encoding="utf-8",
        )

        return verified_dependency_subprocess(
            root,
            closure,
            [
                "git",
                "apply",
                "--whitespace=error-all",
                str(patch_path),
            ],
            verifier,
        )
    finally:
        patch_path.unlink(missing_ok=True)
