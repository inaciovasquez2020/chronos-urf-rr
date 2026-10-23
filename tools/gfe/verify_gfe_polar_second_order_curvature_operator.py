from __future__ import annotations

import json
import sys
from pathlib import Path
import sympy as s

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gfe_polar_second_order_curvature_operator import (
    build_second_order_operator,
    direct_second_order_operator_comparison,
)


def main() -> int:
    data = build_second_order_operator()
    print(json.dumps({
        "schema": "gfe-polar-second-order-stage-receipt-v1",
        "stage": "analytic_second_order_operator_constructed",
        "operator_entries": 36,
        "coefficient": "epsilon**2",
        "passed": True,
        "frontier": "COMPUTED_NOT_YET_INDEPENDENTLY_VERIFIED",
    }, sort_keys=True), flush=True)
    residuals = direct_second_order_operator_comparison(data)
    zero = all(s.simplify(v) == 0 for v in residuals)
    nonzero = [
        {"i": i, "j": j, "residual": str(residuals[i,j])}
        for i in range(6) for j in range(6)
        if s.simplify(residuals[i,j]) != 0
    ]
    print(json.dumps({
        "schema": "gfe-polar-second-order-stage-receipt-v1",
        "stage": "direct_exact_epsilon_squared_operator_comparison",
        "checked_count": 36,
        "passed": zero,
        "frontier": "SECOND_ORDER_OPERATOR_VERIFIED" if zero else "SECOND_ORDER_OPERATOR_VERIFICATION_FAILED",
        "nonzero_residuals": nonzero,
        "quadratic_action_derived": False,
    }, sort_keys=True), flush=True)
    return 0 if zero else 1


if __name__ == "__main__":
    raise SystemExit(main())
