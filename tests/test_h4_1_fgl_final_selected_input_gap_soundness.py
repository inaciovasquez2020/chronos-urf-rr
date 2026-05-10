import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_h4_1_fgl_final_selected_input_gap_soundness_verifier_passes():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_final_selected_input_gap_soundness.py"],
        cwd=ROOT,
        check=True,
    )

def test_h4_1_fgl_final_selected_input_gap_soundness_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/h4_1_fgl_final_selected_input_gap_soundness.json").read_text()
    )
    assert data["status"] == "SELECTED_DOMAIN_GAP_SOUNDNESS_CLOSED"
    assert data["theorem_domain"] == "H4_1_FGL_SelectedTheoremDomain"
    assert "H4_1_FGL_FinalSelectedCarrierGapSoundness" in data["proves"]
    assert data["remaining_frontier"] == "none inside selected-domain H4.1/FGL observation-to-gap/soundness bridge"
    assert "arbitrary semantic final-carrier closure" in data["does_not_claim"]
    assert "P vs NP closure" in data["does_not_claim"]
