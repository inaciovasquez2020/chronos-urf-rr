import subprocess
import sys


def test_restricted_continuation_trace_flux_control_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_trace_flux_control_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "RUNALL_RESTRICTED_CONTINUATION_TRACE_FLUX_CONTROL_LEMMA_OK" in result.stdout
