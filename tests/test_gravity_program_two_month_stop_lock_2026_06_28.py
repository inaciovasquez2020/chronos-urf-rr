import subprocess
import sys

def test_gravity_program_two_month_stop_lock_2026_06_28():
    result = subprocess.run(
        [sys.executable, "tools/verify_gravity_program_two_month_stop_lock_2026_06_28.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "GRAVITY_PROGRAM_TWO_MONTH_STOP_LOCK_2026_06_28_OK" in result.stdout
