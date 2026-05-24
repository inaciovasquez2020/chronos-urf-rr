import subprocess
import sys

def test_external_gravity_input_values_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_external_gravity_input_values.py"],
        check=True,
    )
