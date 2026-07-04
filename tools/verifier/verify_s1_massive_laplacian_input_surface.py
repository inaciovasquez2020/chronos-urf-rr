from pathlib import Path

path = Path("lean/Chronos/Frontier/Gravity/S1MassiveLaplacianInputSurface.lean")
text = path.read_text()

forbidden = [
    "def mathlib_C1_interval_ibp_obligation : Prop := True",
]

for token in forbidden:
    if token in text:
        raise SystemExit(f"FORBIDDEN_OBJECT := {token}")


required = [
    "S1MassiveLaplacianInputSurface",
    "mathlib_C1_interval_ibp_obligation",
    "PeriodicIBPFTCHypotheses",
    "derive_periodic_ibp_from_ftc",
    "ftc_f_boundary_identity",
    "ftc_g_boundary_identity",
    "PeriodicIBPBoundaryCancellation",
    "BOUNDARY_integration_by_parts_derived_from_mathlib",
    "BOUNDARY_pointwise_square_nonnegativity_derived_from_mathlib",
    "BOUNDARY_self_adjointness_proved",
    "BOUNDARY_heat_trace_class_proved",
    "BOUNDARY_spectral_zeta_constructed",
]

missing = [token for token in required if token not in text]
if missing:
    raise SystemExit(f"MISSING_OBJECT := {missing[0]}")

print("S1_MASSIVE_LAPLACIAN_INPUT_SURFACE_OK")
