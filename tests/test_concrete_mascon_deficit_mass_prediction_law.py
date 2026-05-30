import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/concrete_mascon_deficit_mass_prediction_law_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/ConcreteMASCONDeficitMassPredictionLaw.lean")

def test_artifact_boundary():
    artifact = json.loads(ART.read_text())
    assert artifact["prediction_vector_bound"] is False
    assert artifact["model_comparison_executed"] is False
    assert all(artifact["boundary"].values())

def test_lean_contains_boundary_theorem():
    text = LEAN.read_text()
    assert "concreteMASCONDeficitMassPredictionLawBoundary" in text
    assert "noGRFailureClaim" in text
    assert "noDarkMatterReplacementClaim" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_concrete_mascon_deficit_mass_prediction_law.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW_OK" in result.stdout
