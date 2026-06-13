from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_analytic_estimate_derivation_from_pde_inputs_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_analytic_estimate_derivation_from_pde_inputs.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_DERIVATION_FROM_PDE_INPUT_PACKAGE" in result.stdout

def test_restricted_continuation_norm_control_analytic_estimate_derivation_from_pde_inputs_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_ANALYTIC_ESTIMATE_DERIVATION_FROM_PDE_INPUTS_2026_06_13.md").read_text()
    assert "conditional derivation" in text
    assert "does not construct the PDE input package" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION" in text
