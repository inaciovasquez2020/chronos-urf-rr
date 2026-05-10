import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_semantic_observation_map_construction_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_semantic_observation_map_construction.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_semantic_observation_map_construction_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_semantic_observation_map_construction.json").read_text()
    )
    assert data["status"] == "CONDITIONAL_SEMANTIC_CONSTRUCTION"
    assert data["semantic_extraction"] is True
    assert data["condition"] == "explicit separating observable plus one selected final-carrier point"
    assert data["remaining_unconditional_frontier"] == "existence of an explicit separating observable for every selected final-carrier instance"
    assert "unconditional separating observable existence" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
