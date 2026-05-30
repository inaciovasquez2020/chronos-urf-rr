import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_execution_target_2026_05_29.json")
DOC = Path("docs/status/MASCON_MODEL_COMPARISON_EXECUTION_TARGET_2026_05_29.md")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonExecutionTarget.lean")

def test_mascon_model_comparison_target_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["status"] == "MASCON_MODEL_COMPARISON_EXECUTION_TARGET_ONLY_NO_MODEL_RUN"
    assert artifact["schema_validation_passed"] is True
    assert artifact["model_comparison_executed"] is False
    assert artifact["baseline_prediction_vector_bound"] is False
    assert artifact["deficit_mass_prediction_vector_bound"] is False
    assert artifact["comparison_metric_bound"] is False
    assert artifact["weakest_missing_object"] == "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR"
    assert artifact["next_admissible_object"] == "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR"

def test_mascon_model_comparison_target_required_inputs():
    artifact = json.loads(ART.read_text())
    required = set(artifact["required_inputs"])
    assert "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR" in required
    assert "MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR" in required
    assert "MASCON_COMPARISON_METRIC_SPECIFICATION" in required
    assert "MASCON_MODEL_COMPARISON_EXECUTION_RUN" in required

def test_mascon_model_comparison_target_doc_boundary():
    text = DOC.read_text()
    assert "Status: `MASCON_MODEL_COMPARISON_EXECUTION_TARGET_ONLY_NO_MODEL_RUN`" in text
    assert "This is an execution target only." in text
    assert "MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR" in text

def test_mascon_model_comparison_target_lean_boundary():
    text = LEAN.read_text()
    assert "MASCONModelComparisonExecutionTarget" in text
    assert "mascon_model_comparison_not_executed" in text
    assert "mascon_model_comparison_baseline_vector_not_bound" in text
    assert "mascon_model_comparison_status_lock" in text

def test_mascon_model_comparison_target_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_model_comparison_execution_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_MODEL_COMPARISON_EXECUTION_TARGET_OK" in result.stdout
