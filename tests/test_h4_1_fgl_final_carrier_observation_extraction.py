import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_final_carrier_observation_extraction_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_final_carrier_observation_extraction.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_final_carrier_observation_extraction_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_final_carrier_observation_extraction.json").read_text()
    )
    assert data["status"] == "FRONTIER_OPEN"
    assert data["weakest_missing_object"] == "H4_1_FGL_FinalCarrierObservationExtraction"
    assert "P vs NP closure" in data["does_not_claim"]
