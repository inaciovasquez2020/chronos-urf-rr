import subprocess
import sys

def test_urf11_registry_cross_reference():
    subprocess.run(
        [sys.executable, "tools/verify_urf11_registry_cross_reference.py"],
        check=True,
    )
