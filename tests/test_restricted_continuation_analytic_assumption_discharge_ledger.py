import subprocess
import sys


def test_restricted_continuation_analytic_assumption_discharge_ledger_verifier():
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_analytic_assumption_discharge_ledger.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_ANALYTIC_ASSUMPTION_DISCHARGE_LEDGER_OK"
        in result.stdout
    )
