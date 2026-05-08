import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts/chronos/reg_snf_frontier.json"

def test_reg_snf_frontier_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "FRONTIER_OPEN"
    assert data["theorem_closure"] is False
    assert data["weakest_missing_lemma"] is True
    assert data["proves_chronos_rr_closure"] is False

def test_reg_snf_frontier_dependencies_are_separated():
    data = json.loads(ART.read_text())
    assert data["downstream_requires"] == [
        "Reg-Sub-Uniform",
        "Rank-Image-Bound",
        "Depth Bridge",
    ]

def test_reg_snf_frontier_verifier():
    subprocess.run(
        ["python3", "tools/verify_reg_snf_frontier.py"],
        cwd=ROOT,
        check=True,
    )
