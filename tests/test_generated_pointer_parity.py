import subprocess
import sys

def test_generated_pointer_parity():
    r = subprocess.run(
        [sys.executable, "scripts/check_generated_pointer_parity.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "generated-pointer-parity: PASS" in r.stdout
