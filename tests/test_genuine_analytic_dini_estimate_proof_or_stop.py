from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_genuine_analytic_dini_estimate_proof_or_stop_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_genuine_analytic_dini_estimate_proof_or_stop.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GENUINE_ANALYTIC_DINI_ESTIMATE_PROOF_OR_STOP_OK" in result.stdout
