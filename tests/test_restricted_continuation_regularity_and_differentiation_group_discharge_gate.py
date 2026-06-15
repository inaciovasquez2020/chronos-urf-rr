import subprocess
import sys


def test_restricted_continuation_regularity_and_differentiation_group_discharge_gate_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_regularity_and_differentiation_group_discharge_gate.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_REGULARITY_AND_DIFFERENTIATION_GROUP_DISCHARGE_GATE_OK"
        in result.stdout
    )
