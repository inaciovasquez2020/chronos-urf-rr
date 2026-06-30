import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/einstein_hilbert_target_law_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/EinsteinHilbertTargetLawBoundary.lean")

REQUIRED_LEAN_OBJECTS = (
    "structure EinsteinHilbertTargetLawBoundary",
    "theorem einsteinHilbertTargetLawBoundary_preserves_noChronosBridge",
    "structure CarbonBondingMolecularScaleBoundaryLockout",
    "theorem carbonBondingMolecularScaleBoundaryLockout_preserves_noGravityClosure",
    "structure ChronosBridgeStructuralFailureBoundary",
    "theorem chronosBridgeStructuralFailureBoundary_preserves_lockout",
)

REQUIRED_FALSE_LOCKOUTS = (
    "ChronosFieldObject_constructs_metric_stress_energy_action_triple",
    "standard_GR_action_derivation_proves_Chronos_realization",
    "carbon_lattice_stress_defines_global_metric",
    "carbon_lattice_stress_defines_cosmological_stress_energy",
    "molecular_bonding_pressure_closes_gravity",
    "general_relativity_linked_to_chronos_source",
    "solved_gravity",
)

def fail(message: str) -> None:
    print(f"VERIFIER ERROR: {message}")
    sys.exit(1)

def require_false(mapping: dict, key: str) -> None:
    if mapping.get(key) is not False:
        fail(f"'{key}' must be explicitly false.")

def require_true(mapping: dict, key: str) -> None:
    if mapping.get(key) is not True:
        fail(f"'{key}' must be explicitly true.")

def main() -> None:
    if not JSON_PATH.exists():
        fail(f"Target file missing: {JSON_PATH}")
    if not LEAN_PATH.exists():
        fail(f"Lean file missing: {LEAN_PATH}")

    lean_text = LEAN_PATH.read_text()
    for needle in REQUIRED_LEAN_OBJECTS:
        if needle not in lean_text:
            fail(f"Lean object missing: {needle}")

    data = json.loads(JSON_PATH.read_text())
    metadata = data.get("metadata", {})
    if metadata.get("error_codex") != "BR-0104":
        fail("metadata.error_codex must be BR-0104.")

    if metadata.get("boundary") != "¬ standard_GR_action_derivation_supplies_ChronosFieldObject_realization_map":
        fail("metadata.boundary must preserve the standard-GR-is-not-Chronos-realization boundary.")

    target = data.get("standard_gr_target_law")
    if not isinstance(target, dict):
        fail("standard_gr_target_law block must exist.")

    if target.get("object_name") != "EinsteinHilbertTargetLawBoundary":
        fail("standard_gr_target_law.object_name must be EinsteinHilbertTargetLawBoundary.")

    if target.get("role") != "detached_target_boundary":
        fail("standard GR target law must be recorded only as detached_target_boundary.")

    for key in (
        "stationary_action_target_law_recorded",
        "requires_smooth_lorentzian_manifold",
        "requires_active_metric_field",
        "requires_matter_field_state",
        "requires_matter_action",
        "requires_gibbons_hawking_york_boundary_term_for_boundary_well_posedness",
    ):
        require_true(target, key)

    require_false(target, "supplies_chronos_realization_map")

    boundary_list = data.get("carbon_bonding_molecular_scale_boundary_list")
    if not isinstance(boundary_list, dict):
        fail("carbon_bonding_molecular_scale_boundary_list block must exist.")

    carbon = boundary_list.get("carbon_bonding_no_gravity_closure_boundary")
    if not isinstance(carbon, dict):
        fail("carbon_bonding_no_gravity_closure_boundary block must exist.")

    for key in (
        "local_molecular_lattice_stress_defines_global_lorentzian_metric",
        "local_molecular_lattice_stress_defines_cosmological_stress_energy",
        "molecular_bonding_pressure_closes_gravity",
    ):
        require_false(carbon, key)

    target_boundary = boundary_list.get("target_law_asymptotic_boundary")
    if not isinstance(target_boundary, dict):
        fail("target_law_asymptotic_boundary block must exist.")

    require_true(target_boundary, "einstein_hilbert_action_is_detached_target_boundary")
    require_false(target_boundary, "general_relativity_linked_to_chronos_source")

    lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_LOCKOUTS:
        require_false(lockouts, key)

    print("EINSTEIN_HILBERT_TARGET_LAW_BOUNDARY_OK")

if __name__ == "__main__":
    main()
