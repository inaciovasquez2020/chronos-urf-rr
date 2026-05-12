import subprocess
import sys


def test_fiber_large_exists_artifact_verified():
    subprocess.run(
        [sys.executable, "tools/verify_fiber_large_exists.py"],
        check=True,
    )
