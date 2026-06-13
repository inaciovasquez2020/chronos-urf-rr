from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_pde_component_input_constructions_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_pde_component_input_constructions.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_PDE_COMPONENT_INPUT_CONSTRUCTIONS" in result.stdout

def test_restricted_continuation_norm_control_pde_component_input_constructions_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS_2026_06_13.md").read_text()
    assert "conditional component-input construction surface" in text
    assert "does not derive the component analytic estimates" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_COMPONENT_ANALYTIC_ESTIMATES" in text
