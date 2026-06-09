from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_parameter_restricted_external_qk_dini_coefficient_bound_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_parameter_restricted_external_qk_dini_coefficient_bound.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_BOUND_OK" in result.stdout
