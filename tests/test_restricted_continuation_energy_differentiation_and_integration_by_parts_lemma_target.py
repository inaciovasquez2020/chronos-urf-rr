from __future__ import annotations

import subprocess
import sys


def test_runall_restricted_continuation_energy_differentiation_and_integration_by_parts_lemma_target() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "tools/verify_restricted_continuation_energy_differentiation_and_integration_by_parts_lemma_target.py",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (
        "RUNALL_RESTRICTED_CONTINUATION_ENERGY_DIFFERENTIATION_AND_INTEGRATION_BY_PARTS_LEMMA_TARGET_OK"
        in result.stdout
    )
