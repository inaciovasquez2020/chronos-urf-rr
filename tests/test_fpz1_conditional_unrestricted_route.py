import subprocess
import sys

def test_fpz1_conditional_unrestricted_route_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_fpz1_conditional_unrestricted_route.py"],
        check=True,
    )
