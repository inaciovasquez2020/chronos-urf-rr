import subprocess
import sys

def test_fiber_mass_balance_from_nonprop_invariant_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fiber_mass_balance_from_nonprop_invariant.py"],
        check=True,
    )
