import json
import subprocess
from pathlib import Path

ART = Path("artifacts/gravity/shape_compatible_independent_nonzero_baseline_vector_file_2026_05_29.json")

def test_vector_metadata_present():
    artifact = json.loads(ART.read_text())
    assert artifact["baseline_path"] == "data/mascon_vectors/independent_nonzero_baseline_vector.npy"
    assert artifact["baseline_shape"] == [255, 360, 720]
    assert artifact["baseline_size"] == 66096000
    assert artifact["baseline_nonzero"] is True

def test_external_vector_not_fabricated():
    artifact = json.loads(ART.read_text())
    assert artifact["external_gravity_model_status"] == "not_supplied"
    assert artifact["boundary"]["no_external_gravity_model_fabrication"] is True

def test_boundary_lock():
    artifact = json.loads(ART.read_text())
    assert all(artifact["boundary"].values())

def test_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_shape_compatible_independent_nonzero_baseline_vector_file.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "SHAPE_COMPATIBLE_INDEPENDENT_NONZERO_BASELINE_VECTOR_FILE_OK" in result.stdout
