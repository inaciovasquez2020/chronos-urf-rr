import subprocess
import sys

def test_nontrivial_fiber_entropy_gap_strengthening_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_nontrivial_fiber_entropy_gap_strengthening.py"],
        check=True,
    )
