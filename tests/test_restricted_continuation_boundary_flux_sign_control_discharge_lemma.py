import subprocess
import sys


def test_restricted_continuation_boundary_flux_sign_control_discharge_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_boundary_flux_sign_control_discharge_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_FLUX_SIGN_CONTROL_DISCHARGE_LEMMA_OK"
        in result.stdout
    )
