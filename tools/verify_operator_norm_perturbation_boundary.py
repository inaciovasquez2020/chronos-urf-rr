import json
import math
from pathlib import Path

PATH = Path("artifacts/external_validation/operator_norm_perturbation_certificate_2026_06_29.json")
SOURCE = Path("artifacts/external_validation/perturbation_radius_rank_margin_certificate_2026_06_29.json")

REQUIRED_LOCKS = {
    "no_coordinate_perturbation_radius_to_operator_norm_theorem",
    "no_unconditional_rank_stability_theorem",
    "no_unconditional_restricted_continuation_norm_theorem",
    "no_continuous_metric_backreaction_claim",
    "no_gravity_closure",
}

def finite_positive(name, value):
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)) or float(value) <= 0.0:
        raise SystemExit(f"OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL missing_positive_finite::{name}")
    return float(value)

def main():
    if not PATH.exists():
        raise SystemExit(f"OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL missing::{PATH}")
    if not SOURCE.exists():
        raise SystemExit(f"OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL missing_source::{SOURCE}")

    payload = json.loads(PATH.read_text())
    source = json.loads(SOURCE.read_text())

    if payload.get("object") != "supplied_operator_norm_perturbation_bound_certificate":
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL bad_object")

    if payload.get("bridge_status") != "conditional_frontier_surface_only":
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL bad_bridge_status")

    if payload.get("source_boundary") != source.get("object"):
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL bad_source_boundary")

    margin = finite_positive("rank_margin_lower_bound", payload.get("rank_margin_lower_bound"))
    allowed = finite_positive("allowed_operator_perturbation", payload.get("allowed_operator_perturbation"))
    bound = finite_positive("supplied_operator_norm_bound", payload.get("supplied_operator_norm_bound"))

    if margin != finite_positive("source.rank_margin_lower_bound", source.get("rank_margin_lower_bound")):
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL margin_mismatch_with_source")

    if allowed != finite_positive("source.allowed_operator_perturbation", source.get("allowed_operator_perturbation")):
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL allowed_perturbation_mismatch_with_source")

    if not bound <= allowed:
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL operator_norm_bound_exceeds_allowed_perturbation")

    if not allowed < margin:
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL allowed_perturbation_not_below_margin")

    if int(payload.get("numeric_rank")) != 35:
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL bad_numeric_rank")

    if int(payload.get("structural_nullity")) != 1:
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL bad_structural_nullity")

    locks = set(payload.get("locked_out_claims", []))
    missing = sorted(REQUIRED_LOCKS - locks)
    if missing:
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL missing_locks::" + ",".join(missing))

    forbidden = {
        "coordinate_perturbation_radius_to_operator_norm_theorem",
        "rank_stability_theorem",
        "gravity_closure",
        "continuous_metric_backreaction",
    }
    if any(payload.get(key) is True for key in forbidden):
        raise SystemExit("OPERATOR_NORM_PERTURBATION_BOUNDARY_FAIL forbidden_positive_claim")

    print("OPERATOR_NORM_PERTURBATION_BOUNDARY_OK")

if __name__ == "__main__":
    main()
