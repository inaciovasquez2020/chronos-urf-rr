import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_finite_capacity_optical_metric_numerical_witness_verifier():
    subprocess.run(
        ["python3", "tools/verify_finite_capacity_optical_metric_numerical_witness.py"],
        cwd=ROOT,
        check=True,
    )
