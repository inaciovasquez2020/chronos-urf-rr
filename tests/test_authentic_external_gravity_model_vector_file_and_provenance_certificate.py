import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/authentic_external_gravity_model_vector_file_and_provenance_certificate_2026_05_30.json")
LEAN = Path("lean/Chronos/Frontier/AuthenticExternalGravityModelVectorFileAndProvenanceCertificate.lean")

def test_file_and_certificate_not_supplied():
    artifact = json.loads(ART.read_text())
    assert artifact["authentic_external_vector_file_supplied"] is False
    assert artifact["provenance_certificate_supplied"] is False
    assert artifact["shape_compatible"] is False

def test_required_shape():
    artifact = json.loads(ART.read_text())
    assert artifact["required_vector_length"] == 66096000
    assert artifact["required_shape"] == [255, 360, 720]

def test_provenance_fields_required():
    artifact = json.loads(ART.read_text())
    assert all(artifact["required_provenance_certificate_fields"].values())

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_lean_theorems_present():
    text = LEAN.read_text()
    assert "authenticExternalGravityModelVectorFileAndProvenanceCertificate_missing" in text
    assert "authenticExternalGravityModelVectorFileAndProvenanceCertificate_boundary" in text

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_authentic_external_gravity_model_vector_file_and_provenance_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "AUTHENTIC_EXTERNAL_GRAVITY_MODEL_VECTOR_FILE_AND_PROVENANCE_CERTIFICATE_OK" in result.stdout
