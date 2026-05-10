import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_final_selected_input_closure_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_final_selected_input_closure.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_final_selected_input_closure_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_final_selected_input_closure.json").read_text()
    )
    assert data["status"] == "SELECTED_DOMAIN_OBSERVATION_LAYER_CLOSED"
    assert data["new_input"] == "H4_1_FGL_FinalSelectedInput"
    assert data["theorem_domain"] == "H4_1_FGL_SelectedTheoremDomain"
    assert data["remaining_frontier"] == "none inside selected-domain observation-extraction layer"
    assert "arbitrary semantic final-carrier closure" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
