import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/ExternalGravityModelVectorFromAuthenticSourceOrIndependentHoldoutComparisonProtocol.lean")
RUNNER = Path("tools/run_external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol.py")

def test_protocol_branch_selected():
    artifact = json.loads(ART.read_text())
    assert artifact["branch_selected"] == "independent_holdout_comparison_protocol"
    assert artifact["external_gravity_model_vector_supplied"] is False
    assert artifact["independent_holdout_protocol_executed"] is True

def test_holdout_shape():
    artifact = json.loads(ART.read_text())
    holdout = artifact["holdout_selection"]
    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["time_count"] == 51
    assert holdout["holdout_vector_length"] == 13219200

def test_holdout_metrics_positive():
    artifact = json.loads(ART.read_text())
    metrics = artifact["metrics"]
    assert metrics["mean_absolute_delta"] > 0.0
    assert metrics["root_mean_square_delta"] > 0.0
    assert metrics["independent_baseline_nonzero_count"] > 0
    assert metrics["deficit_vector_nonzero_count"] > 0

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "externalGravityModelVectorFromAuthenticSourceOrIndependentHoldoutComparisonProtocol_execution" in text
    assert "externalGravityModelVectorFromAuthenticSourceOrIndependentHoldoutComparisonProtocol_boundary" in text

def test_runner_exists():
    assert RUNNER.exists()

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_external_gravity_model_vector_from_authentic_source_or_independent_holdout_comparison_protocol.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_GRAVITY_MODEL_VECTOR_FROM_AUTHENTIC_SOURCE_OR_INDEPENDENT_HOLDOUT_COMPARISON_PROTOCOL_OK" in result.stdout
