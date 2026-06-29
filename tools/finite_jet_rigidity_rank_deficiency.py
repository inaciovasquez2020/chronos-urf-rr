#!/usr/bin/env python3
"""Diagnostic-only finite-jet rigidity rank-deficiency calculator.

This script computes numerical matrix rank and deficiency for an explicitly
provided numeric matrix. It does not compute an Einstein tensor, metric
backreaction, gravity closure, or overlap-axis eigenvalue mapping.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def rank_deficiency(matrix: np.ndarray, expected_rank: int | None, tolerance: float | None) -> dict:
    if matrix.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    rank = int(np.linalg.matrix_rank(matrix, tol=tolerance))
    max_rank = int(min(matrix.shape))
    reference_rank = max_rank if expected_rank is None else int(expected_rank)
    if reference_rank < 0:
        raise ValueError("expected_rank must be nonnegative")
    return {
        "status": "diagnostic_only",
        "rows": int(matrix.shape[0]),
        "cols": int(matrix.shape[1]),
        "rank": rank,
        "reference_rank": reference_rank,
        "rank_deficiency": int(max(0, reference_rank - rank)),
        "maps_eigenvalue_decay_to_overlap_axis": False,
        "computes_einstein_tensor": False,
        "computes_metric_backreaction": False,
        "claims_gravity_closure": False
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("matrix_json", help="Path to a JSON array of numeric rows")
    parser.add_argument("--expected-rank", type=int, default=None)
    parser.add_argument("--tolerance", type=float, default=None)
    args = parser.parse_args()

    matrix = np.array(json.loads(Path(args.matrix_json).read_text()), dtype=float)
    print(json.dumps(rank_deficiency(matrix, args.expected_rank, args.tolerance), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
