import subprocess
import sys


def test_restricted_continuation_energy_to_norm_control_transfer_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_energy_to_norm_control_transfer_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_ENERGY_TO_NORM_CONTROL_TRANSFER_LEMMA_OK"
        in result.stdout
    )
