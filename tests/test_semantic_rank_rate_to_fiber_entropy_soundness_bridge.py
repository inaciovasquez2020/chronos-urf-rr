import subprocess
import sys

def test_semantic_rank_rate_to_fiber_entropy_soundness_bridge_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_semantic_rank_rate_to_fiber_entropy_soundness_bridge.py"],
        check=True,
    )
