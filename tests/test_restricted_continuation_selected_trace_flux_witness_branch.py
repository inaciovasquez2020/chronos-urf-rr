import subprocess
import sys


def test_restricted_continuation_selected_trace_flux_witness_branch_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_selected_trace_flux_witness_branch.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_SELECTED_TRACE_FLUX_WITNESS_BRANCH_OK"
        in result.stdout
    )
