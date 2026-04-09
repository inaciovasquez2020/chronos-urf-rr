import subprocess
import sys

def test_fgl_unique_assumption_check():
    proc = subprocess.run(
        [sys.executable, "analysis/fgl_unique_assumption_check.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS: FGL is the sole open finite-patch assumption" in proc.stdout
