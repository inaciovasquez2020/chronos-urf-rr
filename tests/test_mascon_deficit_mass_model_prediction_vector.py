import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_deficit_mass_model_prediction_vector_2026_05_29.json")
DOC = Path("docs/status/MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONDeficitMassModelPredictionVector.lean")

def test_mascon_deficit_prediction_vector_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_TARGET_ONLY_NO_LAW"
    assert artifact["baseline_prediction_vector_bound"] is True
    assert artifact["deficit_mass_prediction_vector_bound"] is False
    assert artifact["concrete_deficit_mass_law_bound"] is False
    assert artifact["prediction_vector_materialized"] is False
    assert artifact["comparison_metric_bound"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["weakest_missing_object"] == "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW"
    assert artifact["next_admissible_object"] == "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW"

def test_mascon_deficit_prediction_vector_required_inputs():
    artifact = json.loads(ART.read_text())
    required = set(artifact["required_inputs"])
    assert "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW" in required
    assert "MASCON_GRID_TO_DEFICIT_MASS_OPERATOR" in required
    assert "MASCON_DEFICIT_MASS_VECTOR_GENERATOR" in required
    assert "MASCON_DEFICIT_MASS_VECTOR_DIGEST" in required

def test_mascon_deficit_prediction_vector_doc_boundary():
    text = DOC.read_text()
    assert "Status: `MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_TARGET_ONLY_NO_LAW`" in text
    assert "This is a target object only." in text
    assert "CONCRETE_MASCON_DEFICIT_MASS_PREDICTION_LAW" in text

def test_mascon_deficit_prediction_vector_lean_boundary():
    text = LEAN.read_text()
    assert "MASCONDeficitMassModelPredictionVectorTarget" in text
    assert "mascon_deficit_prediction_vector_not_bound" in text
    assert "mascon_deficit_concrete_law_not_bound" in text
    assert "mascon_deficit_status_lock" in text

def test_mascon_deficit_prediction_vector_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_deficit_mass_model_prediction_vector.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR_TARGET_OK" in result.stdout
