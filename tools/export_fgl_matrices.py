#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


OUT = Path("artifacts/fgl/finite_patch_matrices.json")
STATUS = Path("docs/status/FGL_MATRIX_EXPORT_STATUS_2026_04_27.md")


def fail(msg: str) -> int:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(
        "# FGL matrix export status — 2026-04-27\n\n"
        "Status: Conditional.\n\n"
        f"Blocking object: {msg}\n\n"
        "Required object:\n\n"
        "`artifacts/fgl/finite_patch_matrices.json`\n\n"
        "Required semantics:\n\n"
        "- `field`: exact coefficient field.\n"
        "- `test_matrix_basis_by_test`: basis rows × test columns correlation matrix.\n"
        "- `witness_matrix`: basis rows × witness columns spanning `W_{k,R,B} ⊕ ⟨1⟩`.\n\n",
        encoding="utf-8",
    )
    print(f"MISSING: {msg}", file=sys.stderr)
    return 2


def main() -> int:
    candidates = [
        Path("artifacts/fgl/source_matrices.json"),
        Path("data/fgl/source_matrices.json"),
        Path("docs/data/fgl/source_matrices.json"),
    ]

    src = next((p for p in candidates if p.exists()), None)
    if src is None:
        return fail("source matrix file")

    data = json.loads(src.read_text(encoding="utf-8"))

    required = {"field", "test_matrix_basis_by_test", "witness_matrix"}
    missing = sorted(required - set(data))
    if missing:
        return fail("missing keys: " + ", ".join(missing))

    if data.get("is_placeholder") is True:
        return fail("placeholder matrix file is not admissible")

    T = data["test_matrix_basis_by_test"]
    N = data["witness_matrix"]

    if not isinstance(T, list) or not T or not all(isinstance(r, list) for r in T):
        return fail("test_matrix_basis_by_test must be a nonempty matrix")

    if not isinstance(N, list) or not all(isinstance(r, list) for r in N):
        return fail("witness_matrix must be a matrix")

    basis_size = len(T)
    if len(N) != basis_size:
        return fail("witness_matrix row count must equal basis row count")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "field": data["field"],
        "test_matrix_basis_by_test": T,
        "witness_matrix": N
    }, indent=2) + "\n", encoding="utf-8")

    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(
        "# FGL matrix export status — 2026-04-27\n\n"
        "Status: Exported.\n\n"
        f"Source: `{src}`\n\n"
        f"Output: `{OUT}`\n\n"
        f"Basis rows: {basis_size}\n\n"
        f"Test columns: {len(T[0]) if T else 0}\n\n"
        f"Witness columns: {len(N[0]) if N and N[0] else 0}\n\n",
        encoding="utf-8",
    )

    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
