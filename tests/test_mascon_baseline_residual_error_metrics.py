import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/mascon_baseline_residual_error_metrics_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/MASCONBaselineResidualErrorMetrics.lean")

def test_metric_set():
    artifact = json.loads(ART.read_text())
    assert set(artifact["metrics"]) == {
        "mean_absolute_error",
        "mean_squared_error",
        "root_mean_squared_error",
        "max_absolute_residual",
        "cosine_similarity",
        "pearson_correlation",
    }

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert artifact["numeric_metrics_executed"] is False
    assert artifact["model_comparison_executed"] is False
    assert artifact["empirical_gravity_result"] is False
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "masconBaselineResidualErrorMetrics_vectorLength" in text
    assert "masconBaselineResidualErrorMetrics_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_mascon_baseline_residual_error_metrics.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MASCON_BASELINE_RESIDUAL_ERROR_METRICS_OK" in result.stdout
