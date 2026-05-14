import subprocess
import sys

def test_universal_fiber_entropy_gap_from_counting_and_mass_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_universal_fiber_entropy_gap_from_counting_and_mass.py"],
        check=True,
    )
