from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_qk_dini_source_derived_coefficient_family_interface_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_qk_dini_source_derived_coefficient_family_interface.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "QK_DINI_SOURCE_DERIVED_COEFFICIENT_FAMILY_INTERFACE_OK" in result.stdout
