import subprocess
import sys

def test_gravity_boundary_compactness_collapse_gate_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_gravity_boundary_compactness_collapse_gate.py"],
        check=True,
    )
