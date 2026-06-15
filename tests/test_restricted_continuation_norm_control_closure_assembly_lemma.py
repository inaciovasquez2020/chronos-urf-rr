import subprocess
import sys


def test_restricted_continuation_norm_control_closure_assembly_lemma_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_closure_assembly_lemma.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_CLOSURE_ASSEMBLY_LEMMA_OK"
        in result.stdout
    )
