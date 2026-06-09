from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_concrete_parameter_restricted_external_qk_dini_coefficient_slice_value_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_concrete_parameter_restricted_external_qk_dini_coefficient_slice_value.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "CONCRETE_PARAMETER_RESTRICTED_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_OK" in result.stdout
