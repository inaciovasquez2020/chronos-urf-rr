import subprocess
import sys

def test_counting_with_entropy_mass_to_fiber_mass_balance_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_with_entropy_mass_to_fiber_mass_balance.py"],
        check=True,
    )
