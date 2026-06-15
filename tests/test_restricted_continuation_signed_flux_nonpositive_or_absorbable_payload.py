import subprocess
import sys


def test_restricted_continuation_signed_flux_nonpositive_or_absorbable_payload_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_signed_flux_nonpositive_or_absorbable_payload.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_SIGNED_FLUX_NONPOSITIVE_OR_ABSORBABLE_PAYLOAD_OK"
        in result.stdout
    )
