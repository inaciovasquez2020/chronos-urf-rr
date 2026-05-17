import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_artifact_boundary():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/verified_reduction_frontier_program_2026_05_17.json"
        ).read_text()
    )
    assert data["status"] == "VERIFIED_REDUCTION_FRONTIER_PROGRAM"
    assert data["theorem_promotion"] is False
    assert data["next_frontier"] == "admissible-domain construction excluding zero-gap systems"

def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_verified_reduction_frontier_program.py"],
        cwd=ROOT,
        check=True,
    )
