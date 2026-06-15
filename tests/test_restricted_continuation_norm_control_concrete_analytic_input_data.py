from __future__ import annotations

import subprocess
import sys


def test_runall_concrete_restricted_continuation_norm_control_analytic_input_data_boundary() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_concrete_analytic_input_data.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (
        "RUNALL_CONCRETE_RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_INPUT_DATA_BOUNDARY_OK"
        in result.stdout
    )
