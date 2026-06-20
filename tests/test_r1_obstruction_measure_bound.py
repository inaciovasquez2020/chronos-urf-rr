import subprocess
import sys

def test_r1_obstruction_measure_bound_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_obstruction_measure_bound.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R1_OBSTRUCTION_MEASURE_BOUND_OK" in result.stdout
