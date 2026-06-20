import subprocess
import sys


def test_r1_domain_identity_verifier():
    result = subprocess.run(
        [sys.executable, "tools/verify_r1_domain_identity.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "R1_DOMAIN_IDENTITY_OK" in result.stdout
