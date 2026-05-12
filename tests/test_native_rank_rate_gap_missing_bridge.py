import subprocess
import sys


def test_native_rank_rate_gap_missing_bridge_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_native_rank_rate_gap_missing_bridge.py"],
        check=True,
    )
