from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_concrete_analytic_einstein_matter_estimate_package_target_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_concrete_analytic_einstein_matter_estimate_package_target.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
    assert "TARGET_FORMALIZED_ANALYTIC_PACKAGE_NOT_PROVED" in result.stdout

def test_concrete_analytic_einstein_matter_estimate_package_target_boundaries() -> None:
    status = (ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_TARGET_2026_05_23.md").read_text()
    assert "Does not prove" in status
    assert "concrete analytic Einstein-matter estimate package" in status
    assert "gravity closure" in status
    assert "P vs NP" in status
    assert "any Clay problem" in status
    assert "gravity solved" not in status.lower()
