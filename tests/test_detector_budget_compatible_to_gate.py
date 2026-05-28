import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_detector_budget_compatible_to_gate_verifier():
    result = subprocess.run(
        ["python3", "tools/verify_detector_budget_compatible_to_gate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DETECTOR_BUDGET_COMPATIBLE_TO_GATE_OK" in result.stdout
