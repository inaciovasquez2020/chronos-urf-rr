from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_theta_residual_cross_validation_stability_run_verifier():
    subprocess.run(
        ["python3", "tools/verify_theta_residual_cross_validation_stability_run.py"],
        cwd=ROOT,
        check=True,
    )
