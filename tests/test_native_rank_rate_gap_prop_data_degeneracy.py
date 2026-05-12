import subprocess
import sys


def test_native_rank_rate_gap_prop_data_degeneracy_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_native_rank_rate_gap_prop_data_degeneracy.py"],
        check=True,
    )
