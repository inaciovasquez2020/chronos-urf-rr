import subprocess
import sys

def test_r1_width_threshold_alias_local_placeholder_closure_lock_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_r1_width_threshold_alias_local_placeholder_closure_lock.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R1_WIDTH_THRESHOLD_ALIAS_LOCAL_PLACEHOLDER_CLOSURE_LOCK_OK" in result.stdout
