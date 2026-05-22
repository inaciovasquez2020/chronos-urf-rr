import subprocess
import sys

def test_six_field_analytic_package_hypothesis_frontier_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_six_field_analytic_package_hypothesis_frontier.py"],
        check=True,
    )
