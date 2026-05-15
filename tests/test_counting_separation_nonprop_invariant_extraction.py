import subprocess
import sys


def test_counting_separation_nonprop_invariant_extraction_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_separation_nonprop_invariant_extraction.py"],
        check=True,
    )
