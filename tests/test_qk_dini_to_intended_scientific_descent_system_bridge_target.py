from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "verifier/verify_qk_dini_to_intended_scientific_descent_system_bridge_target.py"

def test_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr
    assert "QK_DINI_TO_INTENDED_SCIENTIFIC_DESCENT_SYSTEM_BRIDGE_TARGET_OK" in result.stdout
