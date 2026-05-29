from pathlib import Path
import subprocess


def test_rotation_curve_prediction_comparison_execution_chain_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_rotation_curve_prediction_comparison_execution_chain.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ROTATION_CURVE_PREDICTION_COMPARISON_EXECUTION_CHAIN_OK" in result.stdout
