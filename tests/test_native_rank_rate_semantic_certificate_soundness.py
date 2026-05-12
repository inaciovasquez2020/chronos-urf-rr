import subprocess
import sys


def test_native_rank_rate_semantic_certificate_soundness_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_native_rank_rate_semantic_certificate_soundness.py"],
        check=True,
    )
