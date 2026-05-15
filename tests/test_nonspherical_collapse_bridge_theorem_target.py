import subprocess
import sys


def test_nonspherical_collapse_bridge_theorem_target_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_nonspherical_collapse_bridge_theorem_target.py"],
        check=True,
    )
