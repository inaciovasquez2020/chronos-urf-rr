from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_nonzero_concrete_qk_dini_coefficient_family_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_nonzero_concrete_qk_dini_coefficient_family.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "NONZERO_CONCRETE_QK_DINI_COEFFICIENT_FAMILY_OK" in result.stdout
