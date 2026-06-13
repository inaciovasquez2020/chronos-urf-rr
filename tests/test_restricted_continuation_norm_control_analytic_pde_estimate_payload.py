from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_analytic_pde_estimate_payload_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_analytic_pde_estimate_payload.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD" in result.stdout

def test_restricted_continuation_norm_control_analytic_pde_estimate_payload_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_2026_06_13.md").read_text()
    assert "conditional analytic PDE estimate payload surface" in text
    assert "does not construct those payload inputs from PDE equations" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION" in text
