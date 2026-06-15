import subprocess
import sys


def test_restricted_continuation_trace_inequality_or_boundary_sign_witness_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_trace_inequality_or_boundary_sign_witness.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_TRACE_INEQUALITY_OR_BOUNDARY_SIGN_WITNESS_OK"
        in result.stdout
    )
