import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/depth_bridge_gap_interface.json"

def test_depth_bridge_gap_interface_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "CONDITIONAL_INTERFACE_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_rr_closure"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False

def test_depth_bridge_gap_interface_missing_object():
    data = json.loads(ART.read_text())
    assert data["proved_conditional"] == "FiberEntropyGap implies RankImageBound"
    assert data["missing_object"] == "FiberEntropyGap"

def test_depth_bridge_gap_interface_verifier():
    subprocess.run(
        ["python3", "tools/verify_depth_bridge_gap_interface.py"],
        cwd=ROOT,
        check=True,
    )
