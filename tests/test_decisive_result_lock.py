import subprocess
import sys

def test_decisive_result_lock_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_decisive_result_lock.py"],
        check=True,
    )
