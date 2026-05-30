import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_real_holdout_dataset_binding_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrRealHoldoutDatasetBinding.lean")

def test_real_holdout_binding_supplied():
    artifact = json.loads(ART.read_text())
    assert artifact["branch_selected"] == "real_holdout_dataset_binding"
    assert artifact["real_holdout_dataset_binding_supplied"] is True
    assert artifact["authentic_external_gravity_model_vector_source_supplied"] is False

def test_authenticated_binding_artifacts_exist():
    artifact = json.loads(ART.read_text())
    assert len(artifact["authenticated_binding_artifacts"]) >= 1
    for item in artifact["authenticated_binding_artifacts"]:
        assert Path(item["path"]).exists()
        assert len(item["sha256"]) == 64

def test_holdout_binding_shape():
    artifact = json.loads(ART.read_text())
    holdout = artifact["holdout_binding"]
    assert holdout["rule"] == "time_index_mod_5_eq_0"
    assert holdout["holdout_vector_length"] == 13219200
    assert holdout["required_vector_length"] == 66096000

def test_metrics_inherited_positive():
    artifact = json.loads(ART.read_text())
    metrics = artifact["inherited_holdout_metrics"]
    assert metrics["mean_absolute_delta"] > 0.0
    assert metrics["root_mean_square_delta"] > 0.0

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "authenticExternalGravityModelVectorSourceOrRealHoldoutDatasetBinding_execution" in text
    assert "authenticExternalGravityModelVectorSourceOrRealHoldoutDatasetBinding_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authentic_external_gravity_model_vector_source_or_real_holdout_dataset_binding.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_REAL_HOLDOUT_DATASET_BINDING_OK" in result.stdout
