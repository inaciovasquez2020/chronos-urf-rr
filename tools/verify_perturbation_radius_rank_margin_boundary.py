import json
import math
from pathlib import Path

PATH = Path("artifacts/external_validation/perturbation_radius_rank_margin_certificate_2026_06_29.json")

REQUIRED_LOCKS = {
    "no_unconditional_rank_stability_theorem",
    "no_coordinate_perturbation_radius_to_operator_norm_theorem",
    "no_unconditional_restricted_continuation_norm_theorem",
    "no_continuous_metric_backreaction_claim",
    "no_gravity_closure",
}

def finite_positive(name, value):
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)) or float(value) <= 0.0:
        raise SystemExit(f"PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL missing_positive_finite::{name}")
    return float(value)

def main():
    if not PATH.exists():
        raise SystemExit(f"PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL missing::{PATH}")

    payload = json.loads(PATH.read_text())

    if payload.get("object") != "perturbation_radius_to_rank_margin_bridge":
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL bad_object")

    if payload.get("bridge_status") != "conditional_frontier_surface_only":
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL bad_bridge_status")

    margin = finite_positive("rank_margin_lower_bound", payload.get("rank_margin_lower_bound"))
    perturbation = finite_positive("allowed_operator_perturbation", payload.get("allowed_operator_perturbation"))

    if not perturbation < margin:
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL perturbation_not_below_margin")

    if int(payload.get("numeric_rank")) != 35:
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL bad_numeric_rank")

    if int(payload.get("structural_nullity")) != 1:
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL bad_structural_nullity")

    locks = set(payload.get("locked_out_claims", []))
    missing = sorted(REQUIRED_LOCKS - locks)
    if missing:
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL missing_locks::" + ",".join(missing))

    forbidden = {
        "rank_stability_theorem",
        "coordinate_radius_to_operator_norm_theorem",
        "gravity_closure",
        "continuous_metric_backreaction",
    }
    if any(payload.get(key) is True for key in forbidden):
        raise SystemExit("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_FAIL forbidden_positive_claim")

    print("PERTURBATION_RADIUS_RANK_MARGIN_BOUNDARY_OK")

if __name__ == "__main__":
    main()
