import subprocess
import sys

def test_counting_fiber_separation_from_fiber_large_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_fiber_separation_from_fiber_large.py"],
        check=True,
    )
