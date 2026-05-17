import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_artifact_boundary():
    data = json.loads(
        (
            ROOT
            / "artifacts/chronos/lyapunov_certificate_unrestricted_obstruction_2026_05_17.json"
        ).read_text()
    )
    assert data["status"] == "UNRESTRICTED_LYAPUNOV_CERTIFICATE_FALSE"
    assert data["theorem_promotion"] is False
    assert data["counterexample"] == "zeroBoundSystem"

def test_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_lyapunov_certificate_unrestricted_obstruction.py"],
        cwd=ROOT,
        check=True,
    )
