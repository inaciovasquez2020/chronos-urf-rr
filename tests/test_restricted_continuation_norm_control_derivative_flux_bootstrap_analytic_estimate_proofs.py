from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_derivative_flux_bootstrap_analytic_estimate_proofs_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_derivative_flux_bootstrap_analytic_estimate_proofs.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS" in result.stdout

def test_restricted_continuation_norm_control_derivative_flux_bootstrap_analytic_estimate_proofs_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS_2026_06_13.md").read_text()
    assert "conditional derivative, flux, and bootstrap analytic estimate proof surface" in text
    assert "does not derive those proof inputs from PDE equations" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_PDE_ESTIMATE_PAYLOAD" in text
