#!/usr/bin/env python3
from pathlib import Path
import sys

LEAN = Path("lean/Chronos/Frontier/LocalAnisotropicTurnaroundInputSurface.lean")
WORKFLOW = Path(".github/workflows/external-status-lock.yml")

FORBIDDEN_EXACT = [
    "gravity_closure",
    "Einstein_limit",
    "new_cosmology_solution",
    "turnaround_radius_proves_gravity",
]

REQUIRED = [
    "structure LocalAnisotropicTurnaroundInputSurface : Type 1 where",
    "Structure : Type",
    "Center : Structure",
    "DistanceMpcX100 : Structure → Nat",
    "RadialVelocityKmS : Structure → Int",
    "HubbleParameterKmSPerMpc : Nat",
    "PeculiarVelocityResidualKmS : Structure → Int",
    "ZeroVelocityRadiusMpcX100 : Nat",
    "SphericalTurnaroundPredictionMpcX100 : Nat",
    "AnisotropicResidual : Structure → Prop",
    "noGravityClosureClaim : Prop",
    "noEinsteinLimitClaim : Prop",
    "noNewCosmologySolutionClaim : Prop",
    "def localAnisotropicTurnaroundReceiptR0MpcX100 : Nat := 96",
    "def localAnisotropicTurnaroundReceiptLocalHubbleKmSPerMpc : Nat := 78",
    "def localAnisotropicTurnaroundReceiptPeculiarVelocityResidualKmS : Nat := 25",
    "structure LocalAnisotropicTurnaroundPredictionInterfaceCandidate : Type 1 where",
    "theorem anisotropic_residual_is_prediction_interface_candidate",
]


def fail(msg: str) -> None:
    print(f"LOCAL_ANISOTROPIC_TURNAROUND_INPUT_SURFACE_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not LEAN.exists():
        fail(f"missing {LEAN}")
    text = LEAN.read_text(encoding="utf-8")

    for needle in REQUIRED:
        if needle not in text:
            fail(f"missing required surface token: {needle}")

    for forbidden in FORBIDDEN_EXACT:
        if forbidden in text:
            fail(f"forbidden overclaim token present: {forbidden}")

    if "axiom " in text or "opaque " in text or "sorry" in text or "admit" in text:
        fail("forbidden Lean escape hatch present")

    if WORKFLOW.exists():
        workflow = WORKFLOW.read_text(encoding="utf-8")
        expected = "python3 tools/verifier/verify_local_anisotropic_turnaround_input_surface.py"
        if expected not in workflow:
            fail("verifier not wired into external-status-lock workflow")

    print("LOCAL_ANISOTROPIC_TURNAROUND_INPUT_SURFACE_OK")


if __name__ == "__main__":
    main()
