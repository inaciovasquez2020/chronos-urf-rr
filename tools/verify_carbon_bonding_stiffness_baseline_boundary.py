#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts/external_validation/carbon_bonding_stiffness_baseline_boundary_2026_06_29.json"
LINKED = [
    ROOT / "artifacts/external_validation/carbon_bonding_same_mass_residual_prediction_2026_06_29.json",
    ROOT / "artifacts/external_validation/carbon_bonding_density_contrast_baseline_boundary_2026_06_29.json",
]

EXPECTED_OBJECT = "CARBON_BONDING_STIFFNESS_BASELINE_BOUNDARY_2026_06_29"
EXPECTED_STATUS = "material_mechanics_baseline_not_gravity_law"

REQUIRED_CONTROLS = [
    "bond order",
    "equilibrium bond length",
    "bond stiffness or force constant",
    "bulk density",
    "bulk modulus",
    "crystal or network geometry",
    "temperature band",
    "pressure band",
    "isotope composition",
    "total mass-energy",
]

REQUIRED_FALSE_NONCLAIMS = [
    "bond_stiffness_proves_gravity_residual",
    "bulk_modulus_proves_metric_backreaction",
    "lennard_jones_proves_covalent_carbon_gravity",
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
    for linked in LINKED:
        if not linked.is_file():
            fail(str(linked.relative_to(ROOT)))

    data = json.loads(TARGET.read_text(encoding="utf-8"))

    if data.get("object") != EXPECTED_OBJECT:
        fail(f"object == {EXPECTED_OBJECT}")
    if data.get("status") != EXPECTED_STATUS:
        fail(f"status == {EXPECTED_STATUS}")

    boundary = data.get("boundary", "")
    for phrase in [
        "material-mechanics controls",
        "not evidence of carbon-bonding metric backreaction",
    ]:
        if phrase not in boundary:
            fail(f"boundary phrase {phrase}")

    mechanics = data.get("mechanics_inputs", {})
    for key in [
        "toy_pair_potential",
        "toy_equilibrium_distance",
        "stiffness_proxy",
        "macroscopic_proxy",
    ]:
        if not mechanics.get(key):
            fail(f"mechanics input {key}")

    if data.get("required_material_controls") != REQUIRED_CONTROLS:
        fail("exact carbon bonding stiffness material controls")

    model_boundary = data.get("required_model_boundary", {})
    for key in [
        "lennard_jones_toy_only",
        "covalent_carbon_requires_covalent_potential_or_measured_stiffness",
        "same_mass_residual_prediction_required",
        "density_contrast_baseline_required",
    ]:
        if model_boundary.get(key) is not True:
            fail(f"{key} == true")

    linked_artifacts = data.get("linked_artifacts", [])
    if linked_artifacts != [str(path.relative_to(ROOT)) for path in LINKED]:
        fail("exact linked residual and density artifacts")

    nonclaims = data.get("verifier_enforced_nonclaims", {})
    for key in REQUIRED_FALSE_NONCLAIMS:
        if nonclaims.get(key) is not False:
            fail(f"{key} == false")

    if data.get("weakest_missing_object") != "same_mass_same_density_carbon_stiffness_residual_protocol":
        fail("weakest missing object same_mass_same_density_carbon_stiffness_residual_protocol")

    print("CARBON_BONDING_STIFFNESS_BASELINE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
