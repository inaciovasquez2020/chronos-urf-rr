import subprocess
import sys


def test_fpz1_rate_thick_domain_gap_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fpz1_rate_thick_domain_gap.py"],
        check=True,
    )
