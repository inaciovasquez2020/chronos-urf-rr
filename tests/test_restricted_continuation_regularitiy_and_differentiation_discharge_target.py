import subprocess
import sys


def test_restricted_continuation_regularitiy_and_differentiation_discharge_target_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_regularitiy_and_differentiation_discharge_target.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_DISCHARGE_TARGET_OK"
        in result.stdout
    )
