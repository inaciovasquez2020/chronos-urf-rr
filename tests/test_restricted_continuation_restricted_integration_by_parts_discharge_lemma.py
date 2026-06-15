import subprocess
import sys


def test_restricted_continuation_restricted_integration_by_parts_discharge_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_restricted_integration_by_parts_discharge_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_RESTRICTED_INTEGRATION_BY_PARTS_DISCHARGE_LEMMA_OK"
        in result.stdout
    )
