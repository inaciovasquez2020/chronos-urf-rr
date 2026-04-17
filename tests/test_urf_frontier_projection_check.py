import subprocess
import sys

def test_urf_frontier_projection_check():
    r = subprocess.run(
        [sys.executable, "scripts/check_urf_frontier_projection.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "projection-check: PASS" in r.stdout
