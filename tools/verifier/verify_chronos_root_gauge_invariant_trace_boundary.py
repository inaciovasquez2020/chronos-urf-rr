import json
import math
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/chronos_root_gauge_invariant_trace_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/ChronosRootGaugeInvariantTraceBoundary.lean")

REQUIRED_LEAN_OBJECTS = (
    "structure ChronosRootGaugeInvariantTraceBoundary",
    "theorem chronosRootGaugeInvariantTraceBoundary_preserves_noGeometry",
    "structure ChronosRootGaugeAdvanceOrderBoundary",
    "theorem chronosRootGaugeAdvanceOrderBoundary_preserves_downstreamLockout",
)

FORBIDDEN_CERTIFICATE_KEYS = (
    "metric_tensor",
    "curvature_tensor",
    "mass_density",
    "spacetime_dimension",
    "ricci_scalar",
    "stress_energy",
    "einstein_tensor",
    "point_mass",
)

REQUIRED_FALSE_PURITY = (
    "metric_tensor_generated",
    "curvature_tensor_generated",
    "mass_density_generated",
    "spacetime_dimension_generated",
    "continuum_limit_completed",
    "solved_gravity",
)

REQUIRED_FALSE_ADVANCE = (
    "continuum_scaling_law_derived",
    "ricci_scalar_derived_from_gauge_trace",
    "stress_energy_derived_from_gauge_trace",
    "point_mass_solution_derived_from_gauge_trace",
)

REQUIRED_FALSE_LOCKOUTS = (
    "chronos_root_gauge_trace_preservation_generates_geometry",
    "chronos_root_spectral_solve_outputs_geometric_objects",
    "chronos_spectral_operator_root_trace_collapses_to_geometry",
    "metric_tensor_generated_from_gauge_trace",
    "curvature_tensor_generated_from_gauge_trace",
    "mass_density_generated_from_gauge_trace",
    "spacetime_dimension_generated_from_gauge_trace",
    "continuum_limit_completed",
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
    if metadata.get("boundary") != "¬ chronos_root_gauge_trace_preservation_generates_geometry":
        fail("metadata.boundary must preserve gauge-trace non-geometry boundary.")

    if metadata.get("active_parent_boundary") != "¬ chronos_root_spectral_solve_outputs_geometric_objects":
        fail("active_parent_boundary must preserve the root spectral solve non-geometry lock.")

    certificate = data.get("gauge_trace_certificate")
    if not isinstance(certificate, dict):
        fail("gauge_trace_certificate block must exist.")

    found = key_contains_forbidden(certificate)
    if found:
        fail(f"gauge_trace_certificate contains forbidden geometric key: {found}")

    if certificate.get("object_name") != "ChronosRootGaugeInvariantTraceBoundary":
        fail("gauge_trace_certificate.object_name must be ChronosRootGaugeInvariantTraceBoundary.")

    require_true(certificate, "coordinate_free")
    require_true(certificate, "trace_preserved")

    before = certificate.get("eigenvalues_before")
    after = certificate.get("eigenvalues_after")
    tau = certificate.get("tau")
    trace_before = certificate.get("trace_before")
    trace_after = certificate.get("trace_after")

    if not isinstance(before, list) or not isinstance(after, list):
        fail("eigenvalues_before and eigenvalues_after must be lists.")

    if sorted(before) != sorted(after):
        fail("gauge transformation must preserve the eigenvalue multiset.")

    if not isinstance(tau, (int, float)) or tau <= 0:
        fail("tau must be a positive numeric value.")

    computed_before = sum(math.exp(-tau * float(value)) for value in before)
    computed_after = sum(math.exp(-tau * float(value)) for value in after)

    if not math.isclose(computed_before, float(trace_before), rel_tol=1e-12, abs_tol=1e-12):
        fail("trace_before does not match eigenvalue calculation.")

    if not math.isclose(computed_after, float(trace_after), rel_tol=1e-12, abs_tol=1e-12):
        fail("trace_after does not match eigenvalue calculation.")

    if not math.isclose(computed_before, computed_after, rel_tol=1e-12, abs_tol=1e-12):
        fail("gauge trace preservation failed.")

    purity = data.get("purity_lockout")
    if not isinstance(purity, dict):
        fail("purity_lockout block must exist.")

    for key in REQUIRED_FALSE_PURITY:
        require_false(purity, key)

    advance = data.get("advance_order")
    if not isinstance(advance, dict):
        fail("advance_order block must exist.")

    if advance.get("current_admissible_target") != "finite_gauge_invariant_trace_preservation":
        fail("current admissible target must be finite_gauge_invariant_trace_preservation.")

    for key in REQUIRED_FALSE_ADVANCE:
        require_false(advance, key)

    lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_LOCKOUTS:
        require_false(lockouts, key)

    print("CHRONOS_ROOT_GAUGE_INVARIANT_TRACE_BOUNDARY_OK")

if __name__ == "__main__":
    main()
