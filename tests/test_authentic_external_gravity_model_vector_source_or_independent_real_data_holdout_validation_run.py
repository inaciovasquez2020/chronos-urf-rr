import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrIndependentRealDataHoldoutValidationRun.lean")
RUNNER = Path("tools/run_authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run.py")

def test_validation_run_executed():
    artifact = json.loads(ART.read_text())
    assert artifact["branch_selected"] == "independent_real_data_holdout_validation_run"
    assert artifact["independent_real_data_holdout_validation_run_executed"] is True
    assert artifact["authentic_external_gravity_model_vector_source_supplied"] is False

def test_holdout_validation_positive():
    artifact = json.loads(ART.read_text())
    holdout = artifact["holdout_validation"]
    assert holdout["holdout_vector_length"] == 13219200
    assert holdout["mean_absolute_delta"] > 0.0
    assert holdout["root_mean_square_delta"] > 0.0
    assert holdout["positive_metric_check_passed"] is True

def test_bound_vector_metadata_recorded():
    artifact = json.loads(ART.read_text())
    assert artifact["bound_vectors"]["independent_baseline_file_exists"] is True
    assert artifact["bound_vectors"]["comparison_vector_file_exists"] is True
    assert artifact["bound_vectors"]["independent_baseline_path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["bound_vectors"]["comparison_vector_path"] == "data/mascon_vectors/deficit_vector.npy"

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "authenticExternalGravityModelVectorSourceOrIndependentRealDataHoldoutValidationRun_execution" in text
    assert "authenticExternalGravityModelVectorSourceOrIndependentRealDataHoldoutValidationRun_boundary" in text

def test_runner_exists():
    assert RUNNER.exists()

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authentic_external_gravity_model_vector_source_or_independent_real_data_holdout_validation_run.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_INDEPENDENT_REAL_DATA_HOLDOUT_VALIDATION_RUN_OK" in result.stdout
