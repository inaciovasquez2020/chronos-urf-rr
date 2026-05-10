import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_observation_extraction_witness_interface_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_observation_extraction_witness_interface.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_observation_extraction_witness_interface_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_observation_extraction_witness_interface.json").read_text()
    )
    assert data["status"] == "WITNESS_INTERFACE_ONLY"
    assert data["new_weakest_missing_object"] == "H4_1_FGL_MissingObservationExtractionWitness"
    assert "construction of the observation-extraction witness" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
