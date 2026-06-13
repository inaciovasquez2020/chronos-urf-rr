from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_analytic_estimate_proof_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_analytic_estimate_proof.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_PROOF_OBJECT_ANALYTIC_ESTIMATE_INPUT_REQUIRED" in result.stdout

def test_restricted_continuation_norm_control_analytic_estimate_proof_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_PROOF_2026_06_13.md").read_text()
    assert "conditional proof object" in text
    assert "does not derive the analytic estimate from PDE inputs" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_DERIVATION_FROM_PDE_INPUTS" in text
