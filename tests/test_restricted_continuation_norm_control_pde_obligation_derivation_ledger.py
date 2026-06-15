from __future__ import annotations

import subprocess
import sys


def test_runall_restricted_continuation_norm_control_pde_obligation_derivation_ledger() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_pde_obligation_derivation_ledger.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_OBLIGATION_DERIVATION_LEDGER_OK"
        in result.stdout
    )
