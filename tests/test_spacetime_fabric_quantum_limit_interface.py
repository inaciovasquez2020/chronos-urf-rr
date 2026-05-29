import subprocess
import sys

def test_spacetime_fabric_quantum_limit_interface() -> None: subprocess.run([sys.executable, "tools/verify_spacetime_fabric_quantum_limit_interface.py"], check=True)
