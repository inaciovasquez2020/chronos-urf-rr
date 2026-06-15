from __future__ import annotations

import subprocess
import sys


def test_runall_restricted_continuation_norm_control_concrete_analytic_input_package() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_concrete_analytic_input_package.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_NORM_CONTROL_CONCRETE_ANALYTIC_INPUT_PACKAGE_OK"
        in result.stdout
    )
