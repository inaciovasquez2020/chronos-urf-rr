import subprocess
from pathlib import Path


def test_observed_rotation_curve_budget_gate_bridge_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_observed_rotation_curve_budget_gate_bridge.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "OBSERVED_ROTATION_CURVE_BUDGET_GATE_BRIDGE_OK" in result.stdout
