import subprocess
import sys


def test_fqp_rank_rate_gap_status_verifier_passes():
    subprocess.run(
        [sys.executable, "tools/verify_fqp_rank_rate_gap_status.py"],
        check=True,
    )
