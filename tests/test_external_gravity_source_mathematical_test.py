import subprocess
import sys

def test_external_gravity_source_mathematical_test_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_external_gravity_source_mathematical_test.py"],
        check=True,
    )
