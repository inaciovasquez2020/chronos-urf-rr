import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_source_or_external_model_comparison_registry_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorSourceOrExternalModelComparisonRegistry.lean")

def test_registry_only_status():
    artifact = json.loads(ART.read_text())
    assert artifact["external_gravity_model_vector_source_supplied"] is False
    assert artifact["external_model_comparison_executable"] is False
    assert artifact["weakest_missing_object"] == "SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE"

def test_candidate_sources_registered():
    artifact = json.loads(ART.read_text())
    assert len(artifact["candidate_external_sources"]) == 5

def test_required_shape():
    artifact = json.loads(ART.read_text())
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "authenticExternalGravityModelVectorSourceOrExternalModelComparisonRegistry_missing" in text
    assert "authenticExternalGravityModelVectorSourceOrExternalModelComparisonRegistry_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authentic_external_gravity_model_vector_source_or_external_model_comparison_registry.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OR_EXTERNAL_MODEL_COMPARISON_REGISTRY_OK" in result.stdout
