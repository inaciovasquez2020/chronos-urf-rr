import subprocess
import sys

def test_canonical_zero_entropy_fiber_gap_minimality_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_canonical_zero_entropy_fiber_gap_minimality.py"],
        check=True,
    )
