from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_pde_input_package_construction_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_pde_input_package_construction.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_PDE_INPUT_PACKAGE_CONSTRUCTION" in result.stdout

def test_restricted_continuation_norm_control_pde_input_package_construction_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_INPUT_PACKAGE_CONSTRUCTION_2026_06_13.md").read_text()
    assert "conditional package-construction surface" in text
    assert "does not derive the component PDE inputs" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PDE_COMPONENT_INPUT_CONSTRUCTIONS" in text
