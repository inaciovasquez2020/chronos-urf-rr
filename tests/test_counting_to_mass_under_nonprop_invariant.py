import subprocess
import sys

def test_counting_to_mass_under_nonprop_invariant_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_to_mass_under_nonprop_invariant.py"],
        check=True,
    )
