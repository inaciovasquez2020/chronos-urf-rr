import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_baseline_gravity_model_prediction_vector_2026_05_29.json")
DOC = Path("docs/status/MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONBaselineGravityModelPredictionVector.lean")

def test_mascon_baseline_prediction_vector_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_BOUND_CONTROL_ONLY"
    assert artifact["baseline_prediction_vector_bound"] is True
    assert artifact["prediction_vector_materialized"] is False
    assert artifact["prediction_vector_generator"] == "constant_zero"
    assert artifact["prediction_value"] == 0.0
    assert artifact["deficit_mass_prediction_vector_bound"] is False
    assert artifact["comparison_metric_bound"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["next_admissible_object"] == "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR"

def test_mascon_baseline_prediction_vector_shape():
    artifact = json.loads(ART.read_text())
    assert artifact["shape"]["time"] > 0
    assert artifact["shape"]["lat"] > 0
    assert artifact["shape"]["lon"] > 0
    assert artifact["vector_length"] == artifact["shape"]["time"] * artifact["shape"]["lat"] * artifact["shape"]["lon"]
    assert len(artifact["vector_generator_sha256"]) == 64

def test_mascon_baseline_prediction_vector_doc_boundary():
    text = DOC.read_text()
    assert "Status: `MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_BOUND_CONTROL_ONLY`" in text
    assert "This is a baseline control vector only." in text
    assert "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR" in text

def test_mascon_baseline_prediction_vector_lean_boundary():
    text = LEAN.read_text()
    assert "MASCONBaselineGravityModelPredictionVector" in text
    assert "mascon_baseline_prediction_vector_bound" in text
    assert "mascon_baseline_model_comparison_not_executed" in text
    assert "mascon_baseline_prediction_vector_status_lock" in text

def test_mascon_baseline_prediction_vector_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_baseline_gravity_model_prediction_vector.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_OK" in result.stdout
