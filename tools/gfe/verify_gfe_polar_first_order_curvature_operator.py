from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as s

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gfe_polar_first_order_curvature_operator import (
    build_first_order_operator,
    direct_epsilon_expansion_comparison,
    verify_background_operator,
    verify_first_order_tensor_identities,
)


def all_zero(value):
    if isinstance(value, s.MatrixBase):
        return all(s.simplify(v) == 0 for v in value)
    if isinstance(value, dict):
        return all(all_zero(v) for v in value.values())
    if isinstance(value, (tuple, list)):
        return all(all_zero(v) for v in value)
    return s.simplify(value) == 0


def main() -> int:
    data = build_first_order_operator()
    tensor = verify_first_order_tensor_identities(data)
    direct = direct_epsilon_expansion_comparison(data)
    background = verify_background_operator(data)

    checks = {
        "inverse_metric_direct_expansion": all_zero(
            tensor["inverse_metric_direct_expansion"]
        ),
        "lowered_riemann_symmetries": all_zero(
            tensor["riemann_symmetry_residuals"]
        ),
        "mixed_riemann_direct_expansion_all_256": (
            direct["riemann_component_count"] == 256
            and all_zero(direct["riemann_residuals"])
        ),
        "lowered_riemann_direct_expansion_all_256": (
            direct["lowered_riemann_component_count"] == 256
            and all_zero(direct["lowered_riemann_residuals"])
        ),
        "operator_direct_expansion_all_36": (
            direct["operator_entry_count"] == 36
            and all_zero(direct["operator_residuals"])
        ),
        "first_inverse_metric_variation_term_all_36": all_zero(
            direct["first_inverse_metric_term_residuals"]
        ),
        "second_inverse_metric_variation_term_all_36": all_zero(
            direct["second_inverse_metric_term_residuals"]
        ),
        "background_operator_contract_eigenvalues": all_zero(background),
    }
    print(json.dumps({
        "schema": "gfe-polar-first-order-curvature-audit-v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "frontier": (
            "FIRST_ORDER_VERIFIED"
            if all(checks.values())
            else "FIRST_ORDER_VERIFICATION_FAILED"
        ),
        "second_order_operator_constructed": False,
    }, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
