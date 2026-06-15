import subprocess
import sys


def test_restricted_continuation_regularity_trace_and_boundary_flux_assumptions_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_regularity_trace_and_boundary_flux_assumptions.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_REGULARITY_TRACE_AND_BOUNDARY_FLUX_ASSUMPTIONS_OK"
        in result.stdout
    )
