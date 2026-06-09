from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_qk_dini_ratio_lower_bound_theorem_interface_no_sorry_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_qk_dini_ratio_lower_bound_theorem_interface_no_sorry.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "QK_DINI_RATIO_LOWER_BOUND_THEOREM_INTERFACE_NO_SORRY_OK" in result.stdout
