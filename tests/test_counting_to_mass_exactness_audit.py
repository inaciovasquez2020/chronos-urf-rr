import subprocess
import sys

def test_counting_to_mass_exactness_audit_verifier():
    subprocess.run(
        [sys.executable, "tools/verify_counting_to_mass_exactness_audit.py"],
        check=True,
    )
