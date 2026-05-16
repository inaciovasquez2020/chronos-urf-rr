import subprocess
import sys


def test_counting_witness_supply_bridge_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_witness_supply_bridge.py"],
        check=True,
    )
