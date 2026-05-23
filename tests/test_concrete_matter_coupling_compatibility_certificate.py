from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_concrete_matter_coupling_compatibility_certificate_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_concrete_matter_coupling_compatibility_certificate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
    assert "CONCRETE_MATTER_COUPLING_COMPATIBILITY_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE" in result.stdout

def test_concrete_matter_coupling_compatibility_certificate_boundary() -> None:
    status = (ROOT / "docs/status/CONCRETE_MATTER_COUPLING_COMPATIBILITY_CERTIFICATE_2026_05_23.md").read_text()
    assert "Does not prove" in status
    assert "gravity closure" in status
    assert "P vs NP" in status
    assert "any Clay problem" in status
    assert "gravity solved" not in status.lower()
