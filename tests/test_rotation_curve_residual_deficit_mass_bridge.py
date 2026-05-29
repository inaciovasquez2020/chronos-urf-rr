from pathlib import Path
import subprocess


def test_rotation_curve_residual_deficit_mass_bridge_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_rotation_curve_residual_deficit_mass_bridge.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ROTATION_CURVE_RESIDUAL_DEFICIT_MASS_BRIDGE_OK" in result.stdout
