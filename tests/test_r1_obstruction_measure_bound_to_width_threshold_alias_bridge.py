import subprocess
import sys

def test_r1_obstruction_measure_bound_to_width_threshold_alias_bridge_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_r1_obstruction_measure_bound_to_width_threshold_alias_bridge.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R1_OBSTRUCTION_MEASURE_BOUND_TO_WIDTH_THRESHOLD_ALIAS_BRIDGE_OK" in result.stdout
