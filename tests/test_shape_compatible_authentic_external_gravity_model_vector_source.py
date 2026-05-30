import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/shape_compatible_authentic_external_gravity_model_vector_source_2026_05_29.json")
LEAN = Path("lean/Chronos/Frontier/ShapeCompatibleAuthenticExternalGravityModelVectorSource.lean")

def test_source_contract_only():
    artifact = json.loads(ART.read_text())
    assert artifact["authentic_external_source_supplied"] is False
    assert artifact["shape_compatible_vector_supplied"] is False
    assert artifact["external_model_comparison_executable"] is False

def test_required_shape_contract():
    artifact = json.loads(ART.read_text())
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]

def test_source_contract_fields_required():
    artifact = json.loads(ART.read_text())
    assert all(artifact["required_source_contract"].values())
    assert len(artifact["accepted_source_classes"]) == 5

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "shapeCompatibleAuthenticExternalGravityModelVectorSource_missing" in text
    assert "shapeCompatibleAuthenticExternalGravityModelVectorSource_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_shape_compatible_authentic_external_gravity_model_vector_source.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "SHAPE_COMPATIBLE_AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_SOURCE_OK" in result.stdout
