import subprocess
import sys


def test_counting_extraction_internal_structure_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_extraction_internal_structure.py"],
        check=True,
    )
