#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/carbon_bond_force_gradient_local_em_lockout_2026_06_29.json")

REQUIRED_BOUNDARIES = {
    "carbon_bond_force_as_energy_gradient_boundary",
    "carbon_bonding_no_gravity_closure_boundary",
}

REQUIRED_LOCKOUTS = {
    "does_not_define_gravitational_source_potential",
    "does_not_define_cosmological_source_potential",
    "does_not_define_macro_magnetic_pole_alignment",
    "does_not_close_metric_backreaction",
}

REQUIRED_FORBIDDEN_MAPPINGS = {
    "local_bond_force_to_gravitational_closure",
    "local_bond_pressure_to_metric_tensor_solution",
    "carbon_bonding_to_cosmological_backreaction",
    "covalent_bonding_to_magnetic_pole_equivalence",
}

FORBIDDEN_AFFIRMATIVE_CLAIMS = [
    "carbon bonding solves gravity",
    "carbon bonds solve gravity",
    "carbon bonding closes gravity",
    "carbon bonding explains spacetime metric backreaction",
    "covalent bonding is magnetic pole alignment",
    "carbon bond force is a gravitational source potential",
    "molecular bonding pressure solves metric backreaction",
]

def fail(message: str) -> None:
    raise SystemExit(f"CARBON_BOND_FORCE_GRADIENT_LOCAL_EM_LOCKOUT_FAIL: {message}")

def main() -> None:
    if not ARTIFACT.exists():
        fail(f"missing artifact {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text())

    if data.get("status") != "boundary_lockout_imposed":
        fail("status is not boundary_lockout_imposed")

    if data.get("scope") != "carbon_bonding_molecular_scale":
        fail("scope is not carbon_bonding_molecular_scale")

    boundaries = data.get("boundaries")
    if not isinstance(boundaries, list):
        fail("boundaries is not a list")

    by_id = {entry.get("id"): entry for entry in boundaries if isinstance(entry, dict)}
    missing = REQUIRED_BOUNDARIES - set(by_id)
    if missing:
        fail(f"missing required boundaries: {sorted(missing)}")

    force_boundary = by_id["carbon_bond_force_as_energy_gradient_boundary"]
    if force_boundary.get("canonical_relation") != "F(r) = -dV/dr":
        fail("force boundary does not use canonical relation F(r) = -dV/dr")

    if force_boundary.get("allowed_interpretation") != "local molecular electromagnetic/effective-potential force law":
        fail("force boundary does not isolate local molecular EM/effective-potential interpretation")

    lockouts = set(force_boundary.get("lockout", []))
    missing_lockouts = REQUIRED_LOCKOUTS - lockouts
    if missing_lockouts:
        fail(f"missing force lockouts: {sorted(missing_lockouts)}")

    gravity_boundary = by_id["carbon_bonding_no_gravity_closure_boundary"]
    forbidden_mappings = set(gravity_boundary.get("forbidden_mappings", []))
    missing_forbidden = REQUIRED_FORBIDDEN_MAPPINGS - forbidden_mappings
    if missing_forbidden:
        fail(f"missing forbidden mappings: {sorted(missing_forbidden)}")

    ranked = data.get("ranked_weakest_gaps")
    if not isinstance(ranked, list) or ranked[:1] != ["carbon_bond_force_as_energy_gradient_boundary"]:
        fail("ranked weakest gaps do not place force-gradient boundary first")

    nonclaims = data.get("nonclaims")
    if not isinstance(nonclaims, list) or len(nonclaims) < 4:
        fail("nonclaims list is missing or too small")

    rendered = json.dumps(data, sort_keys=True).lower()
    for claim in FORBIDDEN_AFFIRMATIVE_CLAIMS:
        if claim in rendered:
            fail(f"forbidden affirmative claim present: {claim}")

    print("CARBON_BOND_FORCE_GRADIENT_LOCAL_EM_LOCKOUT_OK")

if __name__ == "__main__":
    main()
