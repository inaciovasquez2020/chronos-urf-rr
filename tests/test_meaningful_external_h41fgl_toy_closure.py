import subprocess
import sys

def test_meaningful_external_h41fgl_toy_closure_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_meaningful_external_h41fgl_toy_closure.py"],
        check=True,
    )
