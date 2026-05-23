import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_analytic_estimate_conditional_package_verifier():
    subprocess.run(
        ["python3", "tools/verify_restricted_analytic_estimate_conditional_package.py"],
        cwd=ROOT,
        check=True,
    )
