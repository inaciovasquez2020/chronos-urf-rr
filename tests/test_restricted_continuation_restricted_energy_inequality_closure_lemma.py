import subprocess
import sys


def test_restricted_continuation_restricted_energy_inequality_closure_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_restricted_energy_inequality_closure_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_RESTRICTED_ENERGY_INEQUALITY_CLOSURE_LEMMA_OK"
        in result.stdout
    )
