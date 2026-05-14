import subprocess
import sys


def test_fo4_cycle_overlap_open_problem_required_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_cycle_overlap_open_problem_required.py"],
        check=True,
    )
