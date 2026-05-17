import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_artifact_boundary():
    data = json.loads(
        (ROOT / "artifacts/chronos/lyapunov_fiber_bound_route_2026_05_17.json").read_text()
    )
    assert data["status"] == "LYAPUNOV_FIBER_BOUND_ROUTE_ONLY"
    assert data["theorem_promotion"] is False
    assert data["weakest_missing_input"] == "LyapunovFiberBoundData D L B"

def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_lyapunov_fiber_bound_route.py"],
        cwd=ROOT,
        check=True,
    )
