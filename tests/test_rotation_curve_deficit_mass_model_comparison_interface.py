from pathlib import Path
import subprocess


def test_rotation_curve_deficit_mass_model_comparison_interface_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_rotation_curve_deficit_mass_model_comparison_interface.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ROTATION_CURVE_DEFICIT_MASS_MODEL_COMPARISON_INTERFACE_OK" in result.stdout
