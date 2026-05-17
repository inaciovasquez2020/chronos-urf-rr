import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_artifact_boundary():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/lyapunov_fiber_bound_data_certificate_2026_05_17.json"
        ).read_text()
    )
    assert data["status"] == "LYAPUNOV_FIBER_BOUND_DATA_CERTIFICATE_CLOSED"
    assert data["theorem_promotion"] is False
    assert data["main_theorem"] == "LyapunovFiberBoundData_from_certificate"

def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_lyapunov_fiber_bound_data_certificate.py"],
        cwd=ROOT,
        check=True,
    )
