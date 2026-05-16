import subprocess
import sys

def test_fpz1_unrestricted_rate_spectrum_obstruction_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fpz1_unrestricted_rate_spectrum_obstruction.py"],
        check=True,
    )
