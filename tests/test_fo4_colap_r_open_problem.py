import subprocess
import sys

def test_fo4_colap_r_open_problem_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_colap_r_open_problem.py"],
        check=True,
    )
