from __future__ import annotations

import subprocess
import sys


def test_runall_restricted_continuation_pde_to_derivative_identity_lemma_target() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_norm_control_pde_to_derivative_identity_lemma_target.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_PDE_TO_DERIVATIVE_IDENTITY_LEMMA_TARGET_OK"
        in result.stdout
    )
