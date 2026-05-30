import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_deficit_mass_prediction_vector_bound_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONDeficitMassPredictionVectorBound.lean")

def test_vector_shape():
    artifact = json.loads(ART.read_text())
    shape = artifact["shape"]
    assert artifact["vector_length"] == shape["time"] * shape["lat"] * shape["lon"]

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert artifact["model_comparison_executed"] is False
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "masconDeficitMassPredictionVectorBound_shape" in text
    assert "masconDeficitMassPredictionVectorBound_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_deficit_mass_prediction_vector_bound.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_DEFICIT_MASS_PREDICTION_VECTOR_BOUND_OK" in result.stdout
