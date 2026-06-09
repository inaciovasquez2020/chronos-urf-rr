from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_qk_dini_uniform_coefficient_bounds_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_qk_dini_uniform_coefficient_bounds.py"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "QKDINI_UNIFORM_COEFFICIENT_BOUNDS_OK" in result.stdout
