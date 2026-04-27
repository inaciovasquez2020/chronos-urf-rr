import subprocess
import sys

def test_chronos_conditional_frontier_status_guard_passes():
    subprocess.run(
        [sys.executable, "scripts/check_chronos_conditional_frontier_status.py"],
        check=True,
    )
