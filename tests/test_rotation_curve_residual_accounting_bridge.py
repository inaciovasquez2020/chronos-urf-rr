import subprocess
from pathlib import Path


def test_rotation_curve_residual_accounting_bridge_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_rotation_curve_residual_accounting_bridge.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ROTATION_CURVE_RESIDUAL_ACCOUNTING_BRIDGE_OK" in result.stdout
