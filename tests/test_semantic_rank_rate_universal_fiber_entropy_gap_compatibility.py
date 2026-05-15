import subprocess
import sys

def test_semantic_rank_rate_universal_fiber_entropy_gap_compatibility_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_semantic_rank_rate_universal_fiber_entropy_gap_compatibility.py"],
        check=True,
    )
