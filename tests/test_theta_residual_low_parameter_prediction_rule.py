import subprocess
from pathlib import Path

def test_theta_residual_low_parameter_prediction_rule_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_theta_residual_low_parameter_prediction_rule.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "THETA_RESIDUAL_LOW_PARAMETER_PREDICTION_RULE_OK" in result.stdout
