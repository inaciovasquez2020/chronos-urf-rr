import json
import sys
from pathlib import Path

JSON_PATH = Path("artifacts/external_validation/chronos_root_finite_spectral_layer_closeout_boundary_2026_06_30.json")
LEAN_PATH = Path("lean/Chronos/Frontier/ChronosRootFiniteSpectralLayerCloseoutBoundary.lean")

REQUIRED_PARENT_FILES = (
    Path("lean/Chronos/Frontier/ChronosRootSpectralSolveBoundary.lean"),
    Path("lean/Chronos/Frontier/ChronosRootGaugeInvariantTraceBoundary.lean"),
    Path("tools/verifier/verify_chronos_root_spectral_solve_boundary.py"),
    Path("tools/verifier/verify_chronos_root_gauge_invariant_trace_boundary.py"),
)

REQUIRED_LEAN_OBJECTS = (
    "structure ChronosRootFiniteSpectralLayerCloseoutBoundary",
    "theorem chronosRootFiniteSpectralLayerCloseoutBoundary_preserves_noGeometryGravity",
    "structure ChronosRootFiniteSpectralLayerNextGapBoundary",
    "theorem chronosRootFiniteSpectralLayerNextGapBoundary_preserves_externalGap",
)

REQUIRED_TRUE_CLOSEOUT = (
    "root_spectral_solve_boundary_present",
    "gauge_invariant_trace_boundary_present",
    "finite_trace_layer_sealed",
)

REQUIRED_FALSE_CLOSEOUT = (
    "metric_tensor_generated",
    "curvature_tensor_generated",
    "stress_energy_generated",
    "mass_density_generated",
    "spacetime_dimension_generated",
    "continuum_emergence_proved",
    "solved_gravity",
)

REQUIRED_FALSE_NEXT_GAP = (
    "continuum_scaling_input_supplied",
    "geometric_field_constructor_supplied",
    "stress_energy_identification_supplied",
    "gravity_solution_supplied",
)

REQUIRED_FALSE_VERIFIER_LOCKOUTS = (
    "chronos_root_finite_spectral_layer_closeout_generates_geometry_or_gravity",
    "finite_spectral_layer_closeout_proves_continuum_emergence",
    "finite_spectral_layer_closeout_derives_metric_tensor",
    "finite_spectral_layer_closeout_derives_curvature",
    "finite_spectral_layer_closeout_derives_stress_energy",
    "finite_spectral_layer_closeout_solves_gravity",
)

FORBIDDEN_CLOSEOUT_CERTIFICATE_KEYS = (
    "metric_tensor",
    "curvature_tensor",
    "stress_energy",
    "einstein_tensor",
    "mass_density",
    "spacetime_dimension",
    "ricci",
    "point_mass",
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
            for forbidden in FORBIDDEN_CLOSEOUT_CERTIFICATE_KEYS:
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
    for parent in REQUIRED_PARENT_FILES:
        if not parent.exists():
            fail(f"Required parent boundary file missing: {parent}")

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
    if metadata.get("boundary") != "¬ chronos_root_finite_spectral_layer_closeout_generates_geometry_or_gravity":
        fail("metadata.boundary must preserve finite spectral closeout non-geometry/non-gravity boundary.")

    parents = metadata.get("active_parent_boundaries")
    if not isinstance(parents, list):
        fail("metadata.active_parent_boundaries must be a list.")

    for required_parent in (
        "¬ chronos_root_spectral_solve_outputs_geometric_objects",
        "¬ chronos_root_gauge_trace_preservation_generates_geometry",
    ):
        if required_parent not in parents:
            fail(f"Missing active parent boundary: {required_parent}")

    certificate = data.get("closeout_certificate")
    if not isinstance(certificate, dict):
        fail("closeout_certificate block must exist.")

    if certificate.get("object_name") != "ChronosRootFiniteSpectralLayerCloseoutBoundary":
        fail("closeout_certificate.object_name must be ChronosRootFiniteSpectralLayerCloseoutBoundary.")

    if certificate.get("scope") != "finite_root_spectral_trace_layer_only":
        fail("closeout scope must remain finite_root_spectral_trace_layer_only.")

    found = key_contains_forbidden(certificate)
    if found:
        fail(f"closeout_certificate contains forbidden geometric key: {found}")

    for key in REQUIRED_TRUE_CLOSEOUT:
        require_true(certificate, key)

    closeout = data.get("closeout_lockout")
    if not isinstance(closeout, dict):
        fail("closeout_lockout block must exist.")

    for key in REQUIRED_FALSE_CLOSEOUT:
        require_false(closeout, key)

    next_gap = data.get("next_gap_lockout")
    if not isinstance(next_gap, dict):
        fail("next_gap_lockout block must exist.")

    for key in REQUIRED_FALSE_NEXT_GAP:
        require_false(next_gap, key)

    ranked = data.get("ranked_remaining_gaps")
    if not isinstance(ranked, list) or len(ranked) != 4:
        fail("ranked_remaining_gaps must contain exactly four ranked gaps.")

    expected = [
        "continuum_scaling_input_surface",
        "geometric_field_constructor",
        "stress_energy_identification",
        "gravity_solution",
    ]

    for index, expected_gap in enumerate(expected, start=1):
        item = ranked[index - 1]
        if item.get("rank") != index:
            fail(f"ranked gap {expected_gap} has wrong rank.")
        if item.get("gap") != expected_gap:
            fail(f"ranked gap {index} must be {expected_gap}.")
        if item.get("status") != "not_supplied":
            fail(f"ranked gap {expected_gap} must remain not_supplied.")

    verifier_lockouts = data.get("verifier_enforced_lockouts")
    if not isinstance(verifier_lockouts, dict):
        fail("verifier_enforced_lockouts block must exist.")

    for key in REQUIRED_FALSE_VERIFIER_LOCKOUTS:
        require_false(verifier_lockouts, key)

    print("CHRONOS_ROOT_FINITE_SPECTRAL_LAYER_CLOSEOUT_BOUNDARY_OK")

if __name__ == "__main__":
    main()
