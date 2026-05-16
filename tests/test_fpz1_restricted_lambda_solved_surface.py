import subprocess
import sys

def test_fpz1_restricted_lambda_solved_surface_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fpz1_restricted_lambda_solved_surface.py"],
        check=True,
    )
