import subprocess
import sys

def test_urf_frontier_zero_divergence():
    r = subprocess.run(
        [sys.executable, "scripts/check_urf_frontier_zero_divergence.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "urf-frontier-zero-divergence: PASS" in r.stdout
