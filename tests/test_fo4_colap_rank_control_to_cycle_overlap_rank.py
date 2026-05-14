import subprocess
import sys

def test_fo4_colap_rank_control_to_cycle_overlap_rank_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fo4_colap_rank_control_to_cycle_overlap_rank.py"],
        check=True,
    )
