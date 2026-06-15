import subprocess
import sys


def test_restricted_continuation_formal_rr_theorem_proof_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_formal_rr_theorem_proof.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_FORMAL_RR_THEOREM_PROOF_TARGET_OK"
        in result.stdout
    )
