import subprocess
import sys


def test_quasi_local_collapse_dichotomy_conditional_frontier_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_quasi_local_collapse_dichotomy_conditional_frontier.py"],
        check=True,
    )
