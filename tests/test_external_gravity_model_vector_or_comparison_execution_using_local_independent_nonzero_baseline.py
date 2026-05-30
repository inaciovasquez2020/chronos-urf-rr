import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/ExternalGravityModelVectorOrComparisonExecutionUsingLocalIndependentNonzeroBaseline.lean")
RUNNER = Path("tools/run_external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline.py")

def test_local_comparison_execution_recorded():
    artifact = json.loads(ART.read_text())
    assert artifact["external_gravity_model_vector_supplied"] is False
    assert artifact["comparison_execution_using_local_independent_baseline"] is True
    assert artifact["empirical_gravity_result"] is False

def test_vector_metadata_recorded():
    artifact = json.loads(ART.read_text())
    assert artifact["independent_baseline"]["path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["comparison_vector"]["path"] == "data/mascon_vectors/deficit_vector.npy"
    assert artifact["independent_baseline"]["size"] == 66096000
    assert artifact["comparison_vector"]["size"] == 66096000

def test_metrics_present():
    artifact = json.loads(ART.read_text())
    metrics = artifact["metrics"]
    assert metrics["vector_length"] == 66096000
    assert metrics["mean_absolute_delta"] >= 0.0
    assert metrics["root_mean_square_delta"] >= 0.0
    assert metrics["max_absolute_delta"] >= 0.0

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "externalGravityModelVectorOrComparisonExecutionUsingLocalIndependentNonzeroBaseline_execution" in text
    assert "externalGravityModelVectorOrComparisonExecutionUsingLocalIndependentNonzeroBaseline_boundary" in text

def test_runner_exists():
    assert RUNNER.exists()

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_external_gravity_model_vector_or_comparison_execution_using_local_independent_nonzero_baseline.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_GRAVITY_MODEL_VECTOR_OR_COMPARISON_EXECUTION_USING_LOCAL_INDEPENDENT_NONZERO_BASELINE_OK" in result.stdout
