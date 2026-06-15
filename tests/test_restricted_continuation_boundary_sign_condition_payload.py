import subprocess
import sys


def test_restricted_continuation_boundary_sign_condition_payload_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_boundary_sign_condition_payload.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_CONDITION_PAYLOAD_OK"
        in result.stdout
    )
