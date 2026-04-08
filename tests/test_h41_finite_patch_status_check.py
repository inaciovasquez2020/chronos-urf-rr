import subprocess
import sys

def test_h41_finite_patch_status_check():
    proc = subprocess.run(
        [sys.executable, "analysis/h41_finite_patch_status_check.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS: H4.1 finite-patch conditional chain present" in proc.stdout
