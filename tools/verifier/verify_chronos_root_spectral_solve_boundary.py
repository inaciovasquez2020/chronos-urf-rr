import json
import math
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/chronos_root_spectral_solve_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/ChronosRootSpectralSolveBoundary.lean")

REQUIRED_LEAN_OBJECTS = (
    "structure ChronosRootSpectralSolveBoundary",
    "theorem chronosRootSpectralSolveBoundary_preserves_purity",
    "structure ChronosRootSpectralSolveAdvanceOrderBoundary",
    "theorem chronosRootSpectralSolveAdvanceOrderBoundary_preserves_downstreamLockout",
)

FORBIDDEN_CERTIFICATE_KEYS = (
    "metric_tensor",
    "curvature_tensor",
    "mass_density",
    "spacetime_dimension",
    "ricci_scalar",
    "stress_energy",
    "ghy_boundary_term",
    "point_mass_solution",
)

REQUIRED_FALSE_PURITY = (
    "geometric_collapse_claimed",
    "metric_tensor_extracted",
    "curvature_tensor_extracted",
    "mass_density_extracted",
    "spacetime_dimension_extracted",
    "continuum_limit_completed",
    "solved_gravity",
)

REQUIRED_FALSE_ADVANCE = (
    "eigenvalue_distribution_density_derived",
    "discrete_gauge_group_rules_derived",
    "link_deletion_eigenvalue_shift_law_derived",
)

REQUIRED_FALSE_LOCKOUTS = (
    "chronos_root_spectral_solve_outputs_geometric_objects",
    "chronos_spectral_operator_root_trace_collapses_to_geometry",
    "pregeometric_bridge_continuum_limit_completed",
    "metric_tensor_extracted_from_root_trace",
    "curvature_tensor_extracted_from_root_trace",
    "mass_density_extracted_from_root_trace",
    "spacetime_dimension_extracted_from_root_trace",
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

def key_contains_forbidden(value) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered_key = str(key).lower()
            for forbidden in FORBIDDEN_CERTIFICATE_KEYS:
                if forbidden in lowered_key:
                    return forbidden
            found = key_contains_forbidden(item)
            if found:
                return found
    elif isinstance(value, list):
        for item in value:
            found = key_contains_forbidden(item)
            if found:
                return found
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
    if metadata.get("boundary") != "¬ chronos_root_spectral_solve_outputs_geometric_objects":
        fail("metadata.boundary must preserve root spectral solve purity.")

    if metadata.get("active_parent_boundary") != "¬ chronos_spectral_operator_root_trace_collapses_to_geometry":
        fail("active_parent_boundary must preserve the root trace non-collapse lock.")

    certificate = data.get("root_solve_certificate")
    if not isinstance(certificate, dict):
        fail("root_solve_certificate block must exist.")

    found = key_contains_forbidden(certificate)
    if found:
        fail(f"root_solve_certificate contains forbidden geometric key: {found}")

    if certificate.get("object_name") != "ChronosRootSpectralSolveBoundary":
        fail("root_solve_certificate.object_name must be ChronosRootSpectralSolveBoundary.")

    require_true(certificate, "coordinate_free")

    eigenvalues = certificate.get("eigenvalues")
    dimension = certificate.get("dimension")
    tau = certificate.get("tau")
    asserted = certificate.get("asserted_trace_value")

    if not isinstance(dimension, int) or dimension <= 0:
        fail("dimension must be a positive integer.")

    if not isinstance(eigenvalues, list) or len(eigenvalues) != dimension:
        fail("eigenvalues must be a list matching dimension.")

    if not all(isinstance(value, (int, float)) for value in eigenvalues):
        fail("eigenvalues must be numeric.")

    if not isinstance(tau, (int, float)) or tau <= 0:
        fail("tau must be a positive numeric value.")

    if not isinstance(asserted, (int, float)):
        fail("asserted_trace_value must be numeric.")

    computed = sum(math.exp(-tau * float(value)) for value in eigenvalues)
    if not math.isclose(computed, float(asserted), rel_tol=1e-12, abs_tol=1e-12):
        fail(f"trace mismatch: computed {computed!r}, asserted {asserted!r}")

    purity = data.get("purity_lockout")
    if not isinstance(purity, dict):
        fail("purity_lockout block must exist.")

    for key in REQUIRED_FALSE_PURITY:
        require_false(purity, key)

    advance = data.get("advance_order")
    if not isinstance(advance, dict):
        fail("advance_order block must exist.")

    if advance.get("current_admissible_target") != "finite_root_spectral_trace_certificate":
        fail("current admissible target must be finite_root_spectral_trace_certificate.")

    for key in REQUIRED_FALSE_ADVANCE:
        require_false(advance, key)

    lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_LOCKOUTS:
        require_false(lockouts, key)

    print("CHRONOS_ROOT_SPECTRAL_SOLVE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
