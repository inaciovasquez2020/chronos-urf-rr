import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_model_comparison_execution_result_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONModelComparisonExecutionResult.lean")

def test_blocked_execution_status():
    artifact = json.loads(ART.read_text())
    assert artifact["comparison_executable"] is False
    assert artifact["numeric_metrics_executed"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["blocked_by_missing_numeric_payload"] is True

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "masconModelComparisonExecutionResult_blocked" in text
    assert "masconModelComparisonExecutionResult_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_model_comparison_execution_result.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_MODEL_COMPARISON_EXECUTION_RESULT_OK" in result.stdout
