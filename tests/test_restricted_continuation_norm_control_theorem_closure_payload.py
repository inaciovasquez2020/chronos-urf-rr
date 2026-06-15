import subprocess
import sys


def test_restricted_continuation_norm_control_theorem_closure_payload_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_theorem_closure_payload.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_THEOREM_CLOSURE_PAYLOAD_OK"
        in result.stdout
    )
