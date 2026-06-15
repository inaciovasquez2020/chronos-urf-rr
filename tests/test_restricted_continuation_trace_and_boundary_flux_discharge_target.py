import subprocess
import sys


def test_restricted_continuation_trace_and_boundary_flux_discharge_target_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_trace_and_boundary_flux_discharge_target.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_TRACE_AND_BOUNDARY_FLUX_DISCHARGE_TARGET_OK"
        in result.stdout
    )
