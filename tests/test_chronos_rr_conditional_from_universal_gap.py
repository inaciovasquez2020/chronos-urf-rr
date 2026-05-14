import subprocess
import sys

def test_chronos_rr_conditional_from_universal_gap_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_chronos_rr_conditional_from_universal_gap.py"],
        check=True,
    )
