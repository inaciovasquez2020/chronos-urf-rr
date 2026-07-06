#!/usr/bin/env python3
from pathlib import Path
import sys

LEAN = Path("lean/Chronos/Frontier/LocalAnisotropicResidualClassificationReceipt.lean")
FRONTIER = Path("lean/Chronos/Frontier.lean")
WORKFLOW = Path(".github/workflows/external-status-lock.yml")

REQUIRED = [
    "import Chronos.Frontier.LocalAnisotropicTurnaroundObservationReceipt",
    "inductive LocalAnisotropicResidualClass : Type where",
    "| residualGeometrySignalCandidate",
    "| residualNoiseCandidate",
    "| residualUndetermined",
    "structure LocalAnisotropicResidualClassificationReceipt : Type where",
    "residualKmS : Nat",
    "radialVelocityErrorKmS : Nat",
    "distanceErrorVelocityEquivalentKmS : Nat",
    "noiseFloorKmS : Nat",
    "geometrySignalThresholdKmS : Nat",
    "classification : LocalAnisotropicResidualClass",
    "geometrySignalCandidateRule : residualKmS > geometrySignalThresholdKmS",
    "noiseCandidateRule : noiseFloorKmS < geometrySignalThresholdKmS",
    "classificationIsOnlyPredictionInterface : Prop",
    "boundaryNoGravityDerivation : Prop",
    "boundaryNoEinsteinLimit : Prop",
    "boundaryNoNewCosmologySolution : Prop",
    "boundaryNoClassificationGravityProof : Prop",
    "def localAnisotropicResidualClassificationReceipt",
    "residualKmS := localAnisotropicTurnaroundKarachentsev2009Receipt.peculiarVelocityDispersionKmS",
    "noiseFloorKmS :=",
    "geometrySignalThresholdKmS := 20",
    "classification := LocalAnisotropicResidualClass.residualGeometrySignalCandidate",
    "theorem local_anisotropic_residual_classification_receipt_constants",
    "theorem local_anisotropic_residual_classification_receipt_signal_candidate",
    "theorem local_anisotropic_residual_classification_receipt_boundary_only",
]

FORBIDDEN = [
    "classification_proves_gravity",
    "residual_classification_proves_gravity",
    "anisotropic_residual_proves_gravity",
    "gravity_closure",
    "Einstein_limit",
    "new_cosmology_solution",
    "derives_Einstein",
    "solves_cosmology",
    "turnaround_radius_proves_gravity",
]


def fail(msg: str) -> None:
    print(f"LOCAL_ANISOTROPIC_RESIDUAL_CLASSIFICATION_RECEIPT_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not LEAN.exists():
        fail(f"missing {LEAN}")

    text = LEAN.read_text(encoding="utf-8")

    for needle in REQUIRED:
        if needle not in text:
            fail(f"missing required classification token: {needle}")

    for forbidden in FORBIDDEN:
        if forbidden in text:
            fail(f"forbidden overclaim token present: {forbidden}")

    if "axiom " in text or "opaque " in text or "sorry" in text or "admit" in text:
        fail("forbidden Lean escape hatch present")

    if FRONTIER.exists():
        frontier = FRONTIER.read_text(encoding="utf-8")
        expected_import = "import Chronos.Frontier.LocalAnisotropicResidualClassificationReceipt"
        if expected_import not in frontier:
            fail("classification receipt import missing from Chronos.Frontier")

    if WORKFLOW.exists():
        workflow = WORKFLOW.read_text(encoding="utf-8")
        expected_cmd = "python3 tools/verifier/verify_local_anisotropic_residual_classification_receipt.py"
        if expected_cmd not in workflow:
            fail("classification receipt verifier not wired into external-status-lock workflow")

    print("LOCAL_ANISOTROPIC_RESIDUAL_CLASSIFICATION_RECEIPT_OK")


if __name__ == "__main__":
    main()
