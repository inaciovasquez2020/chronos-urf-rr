import subprocess
import sys

def test_honest_ai_frontier_test_protocol_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_honest_ai_frontier_test_protocol.py"],
        check=True,
    )
