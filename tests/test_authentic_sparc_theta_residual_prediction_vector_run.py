from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_authentic_sparc_theta_residual_prediction_vector_run_verifier():
    subprocess.run(
        ["python3", "tools/verify_authentic_sparc_theta_residual_prediction_vector_run.py"],
        cwd=ROOT,
        check=True,
    )
