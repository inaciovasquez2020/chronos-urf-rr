import subprocess
import sys

def test_finite_scaling_invariance_of_detector_extraction():
    subprocess.run(
        [sys.executable, "tools/verify_finite_scaling_invariance_of_detector_extraction.py"],
        check=True,
    )
