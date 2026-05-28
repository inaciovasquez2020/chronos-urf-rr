import subprocess
import sys

def test_gravity_pull_push_actual_value_test():
    subprocess.run(
        [sys.executable, "tools/verify_gravity_pull_push_actual_value_test.py"],
        check=True,
    )
