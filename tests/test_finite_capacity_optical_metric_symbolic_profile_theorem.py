import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_capacity_optical_metric_symbolic_profile_theorem_verifier():
    subprocess.run(
        ["python3", "tools/verify_finite_capacity_optical_metric_symbolic_profile_theorem.py"],
        cwd=ROOT,
        check=True,
    )
