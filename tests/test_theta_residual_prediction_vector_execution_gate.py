import subprocess
from pathlib import Path

def test_theta_residual_prediction_vector_execution_gate_verifier():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", "tools/verify_theta_residual_prediction_vector_execution_gate.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "THETA_RESIDUAL_PREDICTION_VECTOR_EXECUTION_GATE_OK" in result.stdout
