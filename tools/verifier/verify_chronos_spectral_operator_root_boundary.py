import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/chronos_spectral_operator_root_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/ChronosSpectralOperatorRootBoundary.lean")

REQUIRED_LEAN_OBJECTS = (
    "structure ChronosSpectralOperatorRootSource",
    "theorem chronosSpectralOperatorRootSource_preserves_noGeometryLeak",
    "structure ChronosSpectralOperatorRootBoundary",
    "theorem chronosSpectralOperatorRootBoundary_preserves_traceLockout",
    "structure ChronosSpectralOperatorAdvanceOrderBoundary",
    "theorem chronosSpectralOperatorAdvanceOrderBoundary_preserves_order",
)

REQUIRED_TRUE_SOURCE = (
    "event_state_operator_supplied",
    "causal_adjacency_operator_supplied",
    "spectral_weight_operator_supplied",
    "event_indexed_vector_space_supplied",
)

REQUIRED_FALSE_SOURCE = (
    "preexisting_metric_tensor_assumed",
    "molecular_lattice_stress_input_used",
    "smooth_spacetime_manifold_assumed",
)

REQUIRED_TRUE_TRACE = (
    "graph_laplacian_operator_declared",
    "heat_kernel_trace_declared",
    "raw_eigenvalue_trace_representation_declared",
)

REQUIRED_FALSE_DOWNSTREAM = (
    "asymptotic_heat_kernel_coefficients_derived",
    "ricci_scalar_from_spectral_trace_derived",
    "stress_energy_from_spectral_trace_derived",
    "ghy_boundary_term_from_spectral_trace_derived",
    "point_mass_solution_from_spectral_trace_derived",
    "continuum_limit_completed",
    "solved_gravity",
)

REQUIRED_FALSE_LOCKOUTS = (
    "chronos_spectral_operator_root_trace_collapses_to_geometry",
    "pregeometric_bridge_continuum_limit_completed",
    "graph_laplacian_heat_kernel_derives_ricci_scalar",
    "spectral_trace_derives_stress_energy_tensor",
    "spectral_trace_derives_ghy_boundary_term",
    "spectral_trace_generates_point_mass_solution",
    "molecular_lattice_stress_used_as_root_source",
    "solved_gravity",
)

FORBIDDEN_RAW_TRACE_TERMS = (
    "ricci",
    "schwarzschild",
    "stress_energy",
    "stress-energy",
    "bulk_modulus",
    "metric_tensor",
    "ghy",
    "point_mass",
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

def contains_forbidden(value) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            found = contains_forbidden(key)
            if found:
                return found
            found = contains_forbidden(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = contains_forbidden(item)
            if found:
                return found
    elif isinstance(value, str):
        lowered = value.lower()
        for term in FORBIDDEN_RAW_TRACE_TERMS:
            if term in lowered:
                return term
    return None

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
    if metadata.get("boundary") != "¬ chronos_spectral_operator_root_trace_collapses_to_geometry":
        fail("metadata.boundary must preserve the spectral-root non-collapse boundary.")

    if metadata.get("active_parent_boundary") != "¬ pregeometric_bridge_continuum_limit_completed":
        fail("active_parent_boundary must preserve the pregeometric continuum-limit lock.")

    source = data.get("root_source")
    if not isinstance(source, dict):
        fail("root_source block must exist.")

    if source.get("object_name") != "ChronosSpectralOperatorRootSource":
        fail("root_source.object_name must be ChronosSpectralOperatorRootSource.")

    for key in REQUIRED_TRUE_SOURCE:
        require_true(source, key)

    for key in REQUIRED_FALSE_SOURCE:
        require_false(source, key)

    trace = data.get("raw_spectral_trace")
    if not isinstance(trace, dict):
        fail("raw_spectral_trace block must exist.")

    if trace.get("object_name") != "ChronosSpectralOperatorRootBoundary":
        fail("raw_spectral_trace.object_name must be ChronosSpectralOperatorRootBoundary.")

    for key in REQUIRED_TRUE_TRACE:
        require_true(trace, key)

    found = contains_forbidden(trace)
    if found:
        fail(f"raw_spectral_trace contains forbidden downstream term: {found}")

    allowed_terms = trace.get("allowed_terms")
    if not isinstance(allowed_terms, list):
        fail("raw_spectral_trace.allowed_terms must be a list.")

    for required in ("graph_laplacian", "eigenvalues", "heat_kernel_trace"):
        if required not in allowed_terms:
            fail(f"raw_spectral_trace.allowed_terms must contain {required}.")

    downstream = data.get("downstream_lockouts")
    if not isinstance(downstream, dict):
        fail("downstream_lockouts block must exist.")

    for key in REQUIRED_FALSE_DOWNSTREAM:
        require_false(downstream, key)

    order = data.get("advance_order")
    if not isinstance(order, dict):
        fail("advance_order block must exist.")

    if order.get("current_admissible_baseline") != "raw_graph_laplacian_heat_kernel_trace":
        fail("current admissible baseline must be raw_graph_laplacian_heat_kernel_trace.")

    require_true(order, "asymptotic_heat_kernel_coefficients_are_downstream")
    require_true(order, "algebraic_gauge_rules_are_downstream")
    require_true(order, "point_mass_calculation_is_downstream")
    require_false(order, "point_mass_admissible_before_continuum_limit")
    require_false(order, "asymptotic_coefficients_claimed_before_trace_baseline")

    lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_LOCKOUTS:
        require_false(lockouts, key)

    print("CHRONOS_SPECTRAL_OPERATOR_ROOT_BOUNDARY_OK")

if __name__ == "__main__":
    main()
