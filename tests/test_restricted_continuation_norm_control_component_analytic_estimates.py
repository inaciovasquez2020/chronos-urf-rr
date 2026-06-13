from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_component_analytic_estimates_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_component_analytic_estimates.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_COMPONENT_ANALYTIC_ESTIMATES" in result.stdout

def test_restricted_continuation_norm_control_component_analytic_estimates_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES_2026_06_13.md").read_text()
    assert "conditional component analytic estimates surface" in text
    assert "does not derive the derivative identity, flux nonnegativity, or bootstrap-bound analytic estimate proofs" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_DERIVATIVE_FLUX_BOOTSTRAP_ANALYTIC_ESTIMATE_PROOFS" in text
