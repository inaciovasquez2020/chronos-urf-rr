import subprocess
import sys


def test_counting_extraction_prop_only_obstruction_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_extraction_prop_only_obstruction.py"],
        check=True,
    )
