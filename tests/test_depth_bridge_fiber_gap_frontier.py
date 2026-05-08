import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/depth_bridge_fiber_gap_frontier.json"

def test_depth_bridge_fiber_gap_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["theorem_closure"] is False
    assert data["chronos_rr_closure"] is False
    assert data["h41_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False
    assert data["proved_here"] is False

def test_depth_bridge_fiber_constraints_are_exact():
    data = json.loads(ART.read_text())
    assert data["fiber_constraints"] == [
        "uniform_positive_conditional_entropy_gap",
        "subexponential_fiber_multiplicity_distortion",
        "registry_uniform_obstruction_gap",
        "rank_image_defect_survives_scaling",
        "no_factorization_through_vanishing_fibers",
    ]

def test_depth_bridge_fiber_gap_verifier():
    subprocess.run(
        ["python3", "tools/verify_depth_bridge_fiber_gap_frontier.py"],
        cwd=ROOT,
        check=True,
    )
