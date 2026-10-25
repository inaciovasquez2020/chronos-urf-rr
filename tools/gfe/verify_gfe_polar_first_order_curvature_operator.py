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


def emit_stage(stage: str, residuals, count: int) -> bool:
    passed = all_zero(residuals)
    print(json.dumps({
        "schema": "gfe-polar-first-order-stage-receipt-v1",
        "stage": stage,
        "checked_count": count,
        "passed": passed,
        "frontier": "PASS" if passed else "FAIL",
    }, sort_keys=True), flush=True)
    return passed


def main() -> int:
    data = build_first_order_operator()
    tensor = verify_first_order_tensor_identities(data)
    background = verify_background_operator(data)

    preflight = {
        "inverse_metric_direct_expansion": (
            tensor["inverse_metric_direct_expansion"], 16
        ),
        "lowered_riemann_symmetries": (
            tensor["riemann_symmetry_residuals"], 768
        ),
        "background_operator_contract_eigenvalues": (background, 36),
    }
    preflight_passed = {}
    for stage, (residuals, count) in preflight.items():
        preflight_passed[stage] = emit_stage(stage, residuals, count)
    if not all(preflight_passed.values()):
        print(json.dumps({
            "schema": "gfe-polar-first-order-curvature-audit-v1",
            "checks": preflight_passed,
            "passed": sum(preflight_passed.values()),
            "total": len(preflight_passed),
            "frontier": "FIRST_ORDER_VERIFICATION_FAILED",
            "second_order_operator_constructed": False,
        }, indent=2, sort_keys=True), flush=True)
        return 1

    def stage_callback(stage, residuals, count):
        emit_stage(stage, residuals, count)

    direct = direct_epsilon_expansion_comparison(data, progress=stage_callback)

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
