import subprocess
import sys

def test_ai_frontier_test_invitation_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_ai_frontier_test_invitation.py"],
        check=True,
    )
