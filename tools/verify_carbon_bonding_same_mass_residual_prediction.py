#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts/external_validation/carbon_bonding_same_mass_residual_prediction_2026_06_29.json"

EXPECTED_OBJECT = "CARBON_BONDING_SAME_MASS_RESIDUAL_PREDICTION_2026_06_29"
EXPECTED_STATUS = "falsifiable_prediction_boundary_not_established_science"

REQUIRED_CONTROLS = [
    "same total rest mass-energy within declared tolerance",
    "same isotope inventory within declared tolerance",
    "same external geometry within declared tolerance",
    "same temperature band within declared tolerance",
    "same net charge within declared tolerance",
    "same environmental gravitational background within declared tolerance",
]

REQUIRED_BASELINES = [
    "ordinary_mass_energy_baseline_required",
    "newtonian_same_radius_mass_baseline_required",
    "gr_or_stress_energy_baseline_required",
    "same_total_mass_energy_required",
    "independent_holdout_required",
]

REQUIRED_FALSE_NONCLAIMS = [
    "carbon_bonding_to_metric_backreaction_law_proved",
    "metric_backreaction_proved",
    "einstein_limit_proved",
    "stress_energy_realization_proved",
    "new_gravity_law_proved",
    "solved_gravity",
]

def fail(msg: str) -> None:
    raise SystemExit(f"MISSING_OBJECT := {msg}")

def main() -> None:
    if not TARGET.is_file():
        fail(str(TARGET.relative_to(ROOT)))

    data = json.loads(TARGET.read_text(encoding="utf-8"))

    if data.get("object") != EXPECTED_OBJECT:
        fail(f"object == {EXPECTED_OBJECT}")
    if data.get("status") != EXPECTED_STATUS:
        fail(f"status == {EXPECTED_STATUS}")

    boundary = data.get("boundary", "")
    for phrase in [
        "not a carbon-bonding-to-metric-backreaction law",
        "not solved gravity",
    ]:
        if phrase not in boundary:
            fail(f"boundary phrase {phrase}")

    prediction = data.get("prediction", {})
    if prediction.get("claim_type") != "candidate_residual_prediction_only":
        fail("prediction claim_type candidate_residual_prediction_only")

    controls = prediction.get("required_matching_controls", [])
    if controls != REQUIRED_CONTROLS:
        fail("exact same-mass carbon bonding controls")

    measured_quantity = prediction.get("measured_quantity", "")
    if "after subtracting ordinary mass-energy/Newtonian/GR baseline" not in measured_quantity:
        fail("baseline-subtracted measured quantity")

    if prediction.get("null_prediction") != "residual difference is zero within measurement uncertainty":
        fail("explicit null prediction")

    baselines = data.get("baseline_requirements", {})
    for key in REQUIRED_BASELINES:
        if baselines.get(key) is not True:
            fail(f"{key} == true")

    nonclaims = data.get("verifier_enforced_nonclaims", {})
    for key in REQUIRED_FALSE_NONCLAIMS:
        if nonclaims.get(key) is not False:
            fail(f"{key} == false")

    if data.get("weakest_missing_object") != "same_mass_carbon_bonding_residual_measurement_protocol":
        fail("weakest missing object same_mass_carbon_bonding_residual_measurement_protocol")

    print("CARBON_BONDING_SAME_MASS_RESIDUAL_PREDICTION_OK")

if __name__ == "__main__":
    main()
