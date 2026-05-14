import subprocess
import sys

def test_nonprop_final_carrier_invariant_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_nonprop_final_carrier_invariant.py"],
        check=True,
    )
