import subprocess
import sys

def test_r1_width_threshold_alias_frontier_status_index_bridge_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_r1_width_threshold_alias_frontier_status_index_bridge.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R1_WIDTH_THRESHOLD_ALIAS_FRONTIER_STATUS_INDEX_BRIDGE_OK" in result.stdout
