import subprocess
import sys


def test_restricted_continuation_boundary_sign_branch_energy_inequality_insertion_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_boundary_sign_branch_energy_inequality_insertion_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_SIGN_BRANCH_ENERGY_INEQUALITY_INSERTION_LEMMA_OK"
        in result.stdout
    )
