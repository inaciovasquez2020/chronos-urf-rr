#!/usr/bin/env python3
from pathlib import Path
import sys

LEAN = Path("lean/Chronos/Frontier/LocalAnisotropicResidualModelComparisonReceipt.lean")
FRONTIER = Path("lean/Chronos/Frontier.lean")
WORKFLOW = Path(".github/workflows/external-status-lock.yml")

REQUIRED = [
    "import Chronos.Frontier.LocalAnisotropicResidualClassificationReceipt",
    "structure LocalAnisotropicIndependentDatasetReceipt : Type where",
    'sourceTitle := "Cosmicflows-3"',
    'sourceAuthors := "R. Brent Tully, Helene M. Courtois, Jenny G. Sorce"',
    'sourceDoi := "10.3847/0004-6256/152/2/50"',
    "catalogueEntryCount := 17669",
    "supportsGalaxyDistances := True",
    "supportsPeculiarVelocityUse := True",
    "inductive LocalAnisotropicResidualModelVerdict : Type where",
    "| anisotropicResidualAboveSphericalBaseline",
    "| residualWithinNoiseBound",
    "| residualUndetermined",
    "structure LocalAnisotropicResidualModelComparisonReceipt : Type where",
    "observedResidualKmS : Nat",
    "sphericalTurnaroundBaselineResidualKmS : Nat",
    "quantitativeResidualModelKmS : Nat",
    "modelErrorBoundKmS : Nat",
    "noiseFloorKmS : Nat",
    "comparisonThresholdKmS : Nat",
    "observedResidualAboveSphericalBaseline",
    "modelWithinErrorBound",
    "noiseFloorBelowComparisonThreshold",
    "comparisonIsOnlyPredictionInterface : Prop",
    "boundaryNoGravityClosure : Prop",
    "boundaryNoGravityDerivation : Prop",
    "boundaryNoEinsteinLimit : Prop",
    "boundaryNoNewCosmologySolution : Prop",
    "boundaryNoComparisonProvesGravity : Prop",
    "def localAnisotropicResidualModelComparisonReceipt",
    "sphericalTurnaroundBaselineResidualKmS := 0",
    "quantitativeResidualModelKmS := 25",
    "modelErrorBoundKmS := 5",
    "verdict := LocalAnisotropicResidualModelVerdict.anisotropicResidualAboveSphericalBaseline",
    "theorem local_anisotropic_independent_dataset_receipt_constants",
    "theorem local_anisotropic_residual_model_comparison_receipt_constants",
    "theorem local_anisotropic_residual_model_comparison_receipt_verdict",
    "theorem local_anisotropic_residual_model_comparison_receipt_boundary_only",
]

FORBIDDEN = [
    "comparison_proves_gravity",
    "classification_proves_gravity",
    "residual_model_proves_gravity",
    "spherical_baseline_proves_gravity",
    "gravity_closure",
    "Einstein_limit",
    "new_cosmology_solution",
    "derives_Einstein",
    "solves_cosmology",
    "turnaround_radius_proves_gravity",
]


def fail(msg: str) -> None:
    print(f"LOCAL_ANISOTROPIC_RESIDUAL_MODEL_COMPARISON_RECEIPT_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not LEAN.exists():
        fail(f"missing {LEAN}")

    text = LEAN.read_text(encoding="utf-8")

    for needle in REQUIRED:
        if needle not in text:
            fail(f"missing required model-comparison token: {needle}")

    for forbidden in FORBIDDEN:
        if forbidden in text:
            fail(f"forbidden overclaim token present: {forbidden}")

    if "axiom " in text or "opaque " in text or "sorry" in text or "admit" in text:
        fail("forbidden Lean escape hatch present")

    if FRONTIER.exists():
        frontier = FRONTIER.read_text(encoding="utf-8")
        expected_import = "import Chronos.Frontier.LocalAnisotropicResidualModelComparisonReceipt"
        if expected_import not in frontier:
            fail("model comparison receipt import missing from Chronos.Frontier")

    if WORKFLOW.exists():
        workflow = WORKFLOW.read_text(encoding="utf-8")
        expected_cmd = "python3 tools/verifier/verify_local_anisotropic_residual_model_comparison_receipt.py"
        if expected_cmd not in workflow:
            fail("model comparison receipt verifier not wired into external-status-lock workflow")

    print("LOCAL_ANISOTROPIC_RESIDUAL_MODEL_COMPARISON_RECEIPT_OK")


if __name__ == "__main__":
    main()
