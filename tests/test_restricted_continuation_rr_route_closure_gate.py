import subprocess
import sys


def test_restricted_continuation_rr_route_closure_gate_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_rr_route_closure_gate.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "RUNALL_RESTRICTED_CONTINUATION_RR_ROUTE_CLOSURE_GATE_OK" in result.stdout
