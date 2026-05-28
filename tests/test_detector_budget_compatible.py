import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_detector_budget_compatible_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_detector_budget_compatible.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DETECTOR_BUDGET_COMPATIBLE_OK" in result.stdout
