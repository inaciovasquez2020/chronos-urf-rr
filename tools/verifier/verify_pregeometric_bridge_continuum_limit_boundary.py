import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/pregeometric_bridge_continuum_limit_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/PreGeometricBridgeContinuumLimitBoundary.lean")

REQUIRED_LEAN_OBJECTS = (
    "structure DiscreteRelationalNetworkSource",
    "theorem discreteRelationalNetworkSource_preserves_noPreexistingGeometry",
    "structure PreGeometricBridgeContinuumLimitBoundary",
    "theorem preGeometricBridgeContinuumLimitBoundary_preserves_noCompletion",
    "structure PreGeometricBridgeAdvanceOrderBoundary",
    "theorem preGeometricBridgeAdvanceOrderBoundary_preserves_pointMassLockout",
)

REQUIRED_FALSE_OBLIGATIONS = (
    "continuum_limit_exists",
    "lorentzian_signature_recovered",
    "metric_reconstruction_from_discrete_distance_proved",
    "stress_energy_from_weight_fluctuations_proved",
    "ricci_scalar_from_graph_laplacian_heat_kernel_proved",
    "einstein_hilbert_action_from_spectral_partition_proved",
    "ghy_boundary_term_from_spectral_expansion_proved",
    "molecular_isolation_invariant_proved",
    "localized_point_mass_solution_generated",
)

REQUIRED_FALSE_LOCKOUTS = (
    "pregeometric_bridge_continuum_limit_completed",
    "ChronosFieldObject_constructs_metric_stress_energy_action_triple",
    "graph_laplacian_heat_kernel_derives_ricci_scalar",
    "spectral_partition_function_derives_einstein_hilbert_action",
    "spectral_expansion_derives_ghy_boundary_term",
    "weight_fluctuations_derive_stress_energy_tensor",
    "point_mass_solution_generated_from_chronos_network",
    "molecular_lattice_stress_used_as_gravity_source",
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
    if metadata.get("boundary") != "¬ pregeometric_bridge_continuum_limit_completed":
        fail("metadata.boundary must preserve the pregeometric continuum-limit noncompletion boundary.")

    if metadata.get("weakest_missing_object") != "continuum_convergence_proof":
        fail("weakest_missing_object must be continuum_convergence_proof.")

    source = data.get("candidate_source")
    if not isinstance(source, dict):
        fail("candidate_source block must exist.")

    if source.get("object_name") != "DiscreteRelationalNetworkSource":
        fail("candidate_source.object_name must be DiscreteRelationalNetworkSource.")

    require_false(source, "preexisting_smooth_manifold_assumed")
    require_false(source, "preexisting_metric_tensor_assumed")

    bridge = data.get("candidate_bridge")
    if not isinstance(bridge, dict):
        fail("candidate_bridge block must exist.")

    if bridge.get("claim_status") != "proposal_only":
        fail("candidate_bridge.claim_status must be proposal_only.")

    if bridge.get("target") != "MetricStressEnergyActionTriple":
        fail("candidate_bridge.target must be MetricStressEnergyActionTriple.")

    obligations = data.get("proof_obligations")
    if not isinstance(obligations, dict):
        fail("proof_obligations block must exist.")

    for key in REQUIRED_FALSE_OBLIGATIONS:
        require_false(obligations, key)

    order = data.get("advance_order")
    if not isinstance(order, dict):
        fail("advance_order block must exist.")

    if order.get("first_admissible_target") != "graph_laplian_heat_kernel_continuum_expansion_boundary":
        fail("first admissible target must be the graph Laplacian heat-kernel continuum expansion boundary.")

    require_true(order, "point_mass_solution_is_downstream")
    require_false(order, "point_mass_solution_admissible_before_continuum_bridge")

    lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_LOCKOUTS:
        require_false(lockouts, key)

    print("PREGEOMETRIC_BRIDGE_CONTINUUM_LIMIT_BOUNDARY_OK")

if __name__ == "__main__":
    main()
