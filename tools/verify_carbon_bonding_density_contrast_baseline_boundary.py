#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts/external_validation/carbon_bonding_density_contrast_baseline_boundary_2026_06_29.json"
LINKED = ROOT / "artifacts/external_validation/carbon_bonding_same_mass_residual_prediction_2026_06_29.json"

EXPECTED_OBJECT = "CARBON_BONDING_DENSITY_CONTRAST_BASELINE_BOUNDARY_2026_06_29"
EXPECTED_STATUS = "density_baseline_boundary_not_carbon_gravity_proof"

REQUIRED_CONTROLS = [
    "total mass-energy",
    "bulk density",
    "external geometry",
    "isotope composition",
    "temperature band",
    "net charge",
    "environmental gravitational background",
    "nearby density contrast",
]

REQUIRED_FALSE_NONCLAIMS = [
    "gravity_anomaly_proves_carbon_bonding",
    "density_contrast_proves_molecular_composition",
    "carbon_bonding_to_metric_backreaction_law_proved",
    "metric_backreaction_proved",
    "einstein_limit_proved",
    "new_gravity_law_proved",
    "solved_gravity",
]

def fail(msg: str) -> None:
    raise SystemExit(f"MISSING_OBJECT := {msg}")

def main() -> None:
    if not TARGET.is_file():
        fail(str(TARGET.relative_to(ROOT)))
    if not LINKED.is_file():
        fail(str(LINKED.relative_to(ROOT)))

    data = json.loads(TARGET.read_text(encoding="utf-8"))

    if data.get("object") != EXPECTED_OBJECT:
        fail(f"object == {EXPECTED_OBJECT}")
    if data.get("status") != EXPECTED_STATUS:
        fail(f"status == {EXPECTED_STATUS}")

    boundary = data.get("boundary", "")
    for phrase in [
        "gravity anomalies imply density or mass-distribution contrast",
        "not a carbon-bonding-to-metric-backreaction law",
    ]:
        if phrase not in boundary:
            fail(f"boundary phrase {phrase}")

    motivation = data.get("motivation", {})
    if motivation.get("earth_gravity_anomaly_use") != "baseline_control_only":
        fail("earth_gravity_anomaly_use baseline_control_only")
    if motivation.get("allowed_inference") != "density_or_mass_distribution_contrast":
        fail("allowed inference density_or_mass_distribution_contrast")
    if motivation.get("rejected_inference") != "gravity_anomaly_identifies_carbon_bonding_or_metric_backreaction":
        fail("rejected inference gravity_anomaly_identifies_carbon_bonding_or_metric_backreaction")

    if data.get("required_baseline_controls") != REQUIRED_CONTROLS:
        fail("exact density baseline controls")

    if data.get("linked_prediction_artifact") != str(LINKED.relative_to(ROOT)):
        fail("linked same-mass residual prediction artifact")

    nonclaims = data.get("verifier_enforced_nonclaims", {})
    for key in REQUIRED_FALSE_NONCLAIMS:
        if nonclaims.get(key) is not False:
            fail(f"{key} == false")

    if data.get("weakest_missing_object") != "same_density_carbon_bonding_residual_protocol":
        fail("weakest missing object same_density_carbon_bonding_residual_protocol")

    print("CARBON_BONDING_DENSITY_CONTRAST_BASELINE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
