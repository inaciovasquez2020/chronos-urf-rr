import subprocess
import sys


def test_restricted_continuation_boundary_orientation_compatibility_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_boundary_orientation_compatibility_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_ORIENTATION_COMPATIBILITY_LEMMA_OK"
        in result.stdout
    )
