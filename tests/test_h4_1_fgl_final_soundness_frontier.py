import json
from pathlib import Path
import subprocess


def test_h4_1_fgl_final_soundness_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_h4_1_fgl_final_soundness_frontier.py"],
        check=True,
    )


def test_h4_1_fgl_final_soundness_frontier_artifact_boundary():
    artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_final_soundness_frontier.json").read_text())
    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["frontier"] == "H4_1_FGL_FinalCarrierSelectedGapSoundness"
    assert "No UniversalFiberEntropyGap theorem" in artifact["boundary"]


def test_h4_1_fgl_final_soundness_frontier_lean_surface():
    lean = Path("Chronos/Frontier/H4_1_FGL_FinalSoundnessFrontier.lean").read_text()
    assert "H4_1_FGL_FinalCarrierObservationExtraction" in lean
    assert "h4_1_fgl_observation_extraction_to_semantic_gap" in lean
    assert "h4_1_fgl_selected_depth_bridge_semantic_separation" in lean
