import subprocess
import sys


def test_gravitational_constant_input() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_gravitational_constant_input.py"],
        check=True,
    )
