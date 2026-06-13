from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_analytic_pde_estimate_payload_construction_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_analytic_pde_estimate_payload_construction.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION" in result.stdout

def test_restricted_continuation_norm_control_analytic_pde_estimate_payload_construction_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD_CONSTRUCTION_2026_06_13.md").read_text()
    assert "conditional analytic PDE estimate payload construction surface" in text
    assert "does not derive the payload field analytic proofs" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS" in text
