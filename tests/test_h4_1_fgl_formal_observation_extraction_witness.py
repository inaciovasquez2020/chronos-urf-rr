import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_formal_observation_extraction_witness_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_formal_observation_extraction_witness.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_formal_observation_extraction_witness_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_formal_observation_extraction_witness.json").read_text()
    )
    assert data["status"] == "FORMAL_PROP_COMPLETION_ONLY"
    assert data["semantic_extraction"] is False
    assert "H4_1_FGL_MissingObservationExtractionWitness" in data["closed_formal_targets"]
    assert data["remaining_semantic_frontier"] == "semantic observation-map construction"
    assert "semantic observation map construction" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
