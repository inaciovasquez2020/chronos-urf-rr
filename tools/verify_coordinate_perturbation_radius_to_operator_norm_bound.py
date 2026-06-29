#!/usr/bin/env python3
import json
import math
from pathlib import Path

CERT = Path("artifacts/external_validation/coordinate_perturbation_radius_to_operator_norm_bound_certificate_2026_06_29.json")

REQUIRED_LOCKS = {
    "no_unconditional_rank_stability_theorem",
    "no_json_as_lean_theorem",
    "no_smooth_differentiable_manifold_theorem",
    "no_continuous_metric_tensor_field_law",
    "no_gravity_closure",
}

def fail(message: str) -> None:
    raise SystemExit(f"COORDINATE_PERTURBATION_RADIUS_TO_OPERATOR_NORM_BOUND_ERROR: {message}")

def positive_finite_number(value) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value)) and float(value) > 0.0

def positive_int(value) -> bool:
    return isinstance(value, int) and value > 0

def main() -> None:
    if not CERT.exists():
        fail(f"missing certificate: {CERT}")

    payload = json.loads(CERT.read_text())

    if payload.get("object") != "coordinate_perturbation_radius_to_operator_norm_bound_certificate":
        fail("bad object")
    if payload.get("bridge_status") != "conditional_frontier_surface_only":
        fail("bad bridge_status")
    if payload.get("claim_boundary") != "certificate_supplies_operator_norm_upper_bound_only":
        fail("bad claim_boundary")

    inputs = payload.get("inputs")
    metrics = payload.get("metrics")
    locks = payload.get("locked_out_claims")

    if not isinstance(inputs, dict):
        fail("inputs must be an object")
    if not isinstance(metrics, dict):
        fail("metrics must be an object")
    if not isinstance(locks, list):
        fail("locked_out_claims must be a list")

    missing_locks = sorted(REQUIRED_LOCKS - set(locks))
    if missing_locks:
        fail(f"missing locked_out_claims: {missing_locks}")

    coordinate_delta_x = inputs.get("coordinate_delta_x")
    node_count = inputs.get("node_count")
    ambient_dimension = inputs.get("ambient_dimension")
    jet_order = inputs.get("jet_order")
    block_dimension = inputs.get("block_dimension")
    local_lipschitz_constant = inputs.get("local_lipschitz_constant")
    supplied_operator_norm_upper_bound = metrics.get("supplied_operator_norm_upper_bound")

    if not positive_finite_number(coordinate_delta_x):
        fail("coordinate_delta_x must be positive finite")
    if not positive_finite_number(local_lipschitz_constant):
        fail("local_lipschitz_constant must be positive finite")
    if not positive_finite_number(supplied_operator_norm_upper_bound):
        fail("supplied_operator_norm_upper_bound must be positive finite")

    for name, value in (
        ("node_count", node_count),
        ("ambient_dimension", ambient_dimension),
        ("jet_order", jet_order),
        ("block_dimension", block_dimension),
    ):
        if not positive_int(value):
            fail(f"{name} must be a positive integer")

    expected_block_dimension = ambient_dimension * (jet_order + 1)
    if block_dimension != expected_block_dimension:
        fail(f"block_dimension mismatch: {block_dimension} != {expected_block_dimension}")

    expected_bound = (
        float(node_count)
        * float(block_dimension)
        * float(local_lipschitz_constant)
        * float(coordinate_delta_x)
    )

    if abs(float(supplied_operator_norm_upper_bound) - expected_bound) > 1e-12:
        fail(
            "operator norm bound mismatch: "
            f"supplied={supplied_operator_norm_upper_bound}, expected={expected_bound}"
        )

    if metrics.get("operator_norm_upper_bound_formula") != "node_count * block_dimension * local_lipschitz_constant * coordinate_delta_x":
        fail("bad operator_norm_upper_bound_formula")

    if metrics.get("is_finite_matrix_diagnostic") is not True:
        fail("is_finite_matrix_diagnostic must be true")

    governing_locks = payload.get("governing_locks")
    if not isinstance(governing_locks, dict):
        fail("governing_locks must be an object")

    if governing_locks.get("terminal_assumption") != "FGL_k_R_B":
        fail("bad terminal_assumption")

    if governing_locks.get("status_lock") != "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF":
        fail("bad status_lock")

    print("COORDINATE_PERTURBATION_RADIUS_TO_OPERATOR_NORM_BOUND_OK")
    print(f"SUPPLIED_OPERATOR_NORM_UPPER_BOUND := {supplied_operator_norm_upper_bound}")
    print("BOUNDARY := ¬ global_rank_stability_theorem")

if __name__ == "__main__":
    main()
