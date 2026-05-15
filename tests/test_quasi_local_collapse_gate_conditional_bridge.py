import subprocess
import sys


def test_quasi_local_collapse_gate_conditional_bridge_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_quasi_local_collapse_gate_conditional_bridge.py"],
        check=True,
    )
