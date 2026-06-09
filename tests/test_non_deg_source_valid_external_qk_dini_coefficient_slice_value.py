from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_non_deg_source_valid_external_qk_dini_coefficient_slice_value_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_non_deg_source_valid_external_qk_dini_coefficient_slice_value.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NONDEGENERATE_SOURCE_VALID_EXTERNAL_QK_DINI_COEFFICIENT_SLICE_VALUE_OK" in result.stdout
