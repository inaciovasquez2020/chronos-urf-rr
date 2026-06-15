import subprocess
import sys


def test_restricted_continuation_boundary_term_discharge_in_restricted_energy_inequality_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_boundary_term_discharge_in_restricted_energy_inequality.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_BOUNDARY_TERM_DISCHARGE_IN_RESTRICTED_ENERGY_INEQUALITY_OK"
        in result.stdout
    )
