#!/usr/bin/env python3
import json
from pathlib import Path

ARTIFACT = Path("artifacts/external_validation/carbon_molecular_scale_repulsion_pressure_magnet_lockout_2026_06_29.json")

REQUIRED_BOUNDARIES = {
    "carbon_bond_short_range_repulsion_boundary",
    "carbon_lattice_pressure_response_boundary",
    "carbon_bonding_no_magnetic_pole_equivalence_boundary",
}

REQUIRED_REPULSION_INTERPRETATIONS = {
    "electron_cloud_overlap_resistance",
    "pauli_exclusion_compression_resistance",
    "electron_electron_coulomb_repulsion",
    "nucleus_nucleus_coulomb_repulsion",
}

REQUIRED_REPULSION_LOCKOUTS = {
    "does_not_introduce_new_fundamental_force",
    "does_not_close_gravity",
    "does_not_close_metric_backreaction",
    "does_not_equate_to_magnetic_pole_alignment",
}

REQUIRED_PRESSURE_TERMS = {
    "local_bond_energy_curvature",
    "lattice_aggregation_rule",
    "stress_or_bulk_modulus_output",
}

REQUIRED_PRESSURE_LOCKOUTS = {
    "does_not_infer_pressure_from_single_bond_without_aggregation",
    "does_not_infer_bulk_modulus_without_lattice_energy_density",
    "does_not_map_local_pressure_to_spacetime_metric_solution",
}

REQUIRED_MAGNET_FORBIDDEN = {
    "covalent_bonding_as_macro_magnetic_pole_alignment",
    "carbon_bond_attraction_as_bar_magnet_pole_force",
    "carbon_bond_repulsion_as_bar_magnet_pole_force",
    "bond_order_as_lorentz_force_closure",
}

FORBIDDEN_AFFIRMATIVE_CLAIMS = [
    "carbon bonding solves gravity",
    "carbon bonds solve gravity",
    "carbon bonding closes gravity",
    "carbon bonding solves metric backreaction",
    "carbon bonding explains spacetime metric backreaction",
    "carbon bonding is magnetic pole alignment",
    "covalent bonding is magnetic pole alignment",
    "carbon bond repulsion is a new fundamental force",
    "single bond derives bulk modulus",
    "gravity sensor chemically identifies carbon hybridization",
]

def fail(message: str) -> None:
    raise SystemExit(f"CARBON_MOLECULAR_SCALE_REPULSION_PRESSURE_MAGNET_LOCKOUT_FAIL: {message}")

def require_set(container, required, label: str) -> None:
    observed = set(container or [])
    missing = required - observed
    if missing:
        fail(f"missing {label}: {sorted(missing)}")

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

    repulsion = by_id["carbon_bond_short_range_repulsion_boundary"]
    require_set(repulsion.get("allowed_interpretation"), REQUIRED_REPULSION_INTERPRETATIONS, "repulsion interpretations")
    require_set(repulsion.get("lockout"), REQUIRED_REPULSION_LOCKOUTS, "repulsion lockouts")

    pressure = by_id["carbon_lattice_pressure_response_boundary"]
    require_set(pressure.get("required_bridge_terms"), REQUIRED_PRESSURE_TERMS, "pressure bridge terms")
    require_set(pressure.get("lockout"), REQUIRED_PRESSURE_LOCKOUTS, "pressure lockouts")

    magnet = by_id["carbon_bonding_no_magnetic_pole_equivalence_boundary"]
    if magnet.get("allowed_use") != "heuristic_analogy_only":
        fail("magnet boundary does not restrict magnet language to heuristic_analogy_only")
    require_set(magnet.get("forbidden_equivalences"), REQUIRED_MAGNET_FORBIDDEN, "magnet forbidden equivalences")

    ranked = data.get("ranked_weakest_gaps")
    if ranked != [
        "carbon_bond_short_range_repulsion_boundary",
        "carbon_lattice_pressure_response_boundary",
        "carbon_bonding_no_magnetic_pole_equivalence_boundary",
    ]:
        fail("ranked weakest gaps do not match selected order")

    nonclaims = data.get("nonclaims")
    if not isinstance(nonclaims, list) or len(nonclaims) < 6:
        fail("nonclaims list is missing or too small")

    rendered = json.dumps(data, sort_keys=True).lower()
    for claim in FORBIDDEN_AFFIRMATIVE_CLAIMS:
        if claim in rendered:
            fail(f"forbidden affirmative claim present: {claim}")

    print("CARBON_MOLECULAR_SCALE_REPULSION_PRESSURE_MAGNET_LOCKOUT_OK")

if __name__ == "__main__":
    main()
