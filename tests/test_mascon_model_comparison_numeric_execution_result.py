import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_numeric_execution_result_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonNumericExecutionResult.lean")

def test_numeric_execution_artifact():
    artifact = json.loads(ART.read_text())
    assert artifact["numeric_metrics_executed"] is True
    assert artifact["model_comparison_executed"] is True
    assert artifact["empirical_gravity_result"] is False
    assert artifact["vector_length"] == 66096000

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_metrics_present():
    metrics = json.loads(ART.read_text())["metrics"]
    assert "mean_absolute_error" in metrics
    assert "root_mean_squared_error" in metrics
    assert "max_absolute_residual" in metrics

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "masconModelComparisonNumericExecutionResult_executed" in text
    assert "masconModelComparisonNumericExecutionResult_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_model_comparison_numeric_execution_result.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_MODEL_COMPARISON_NUMERIC_EXECUTION_RESULT_OK" in result.stdout
