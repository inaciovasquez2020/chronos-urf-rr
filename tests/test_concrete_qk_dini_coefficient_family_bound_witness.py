from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_concrete_qk_dini_coefficient_family_bound_witness_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_concrete_qk_dini_coefficient_family_bound_witness.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_QK_DINI_COEFFICIENT_FAMILY_BOUND_WITNESS_OK" in result.stdout
