from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_remaining_restricted_gravity_certificates_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_remaining_restricted_gravity_certificates.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
    assert "RESTRICTED_CONTINUATION_UNTIL_THRESHOLD_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE" in result.stdout
    assert "RESTRICTED_COLLAPSE_GATE_TRIGGER_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE" in result.stdout
    assert "RESTRICTED_EINSTEIN_MATTER_BOOTSTRAP_PACKAGE_CERTIFICATE_ONLY_NO_GRAVITY_CLOSURE" in result.stdout

def test_remaining_restricted_gravity_certificates_boundaries() -> None:
    docs = [
        ROOT / "docs/status/RESTRICTED_CONTINUATION_UNTIL_THRESHOLD_CERTIFICATE_2026_05_23.md",
        ROOT / "docs/status/RESTRICTED_COLLAPSE_GATE_TRIGGER_CERTIFICATE_2026_05_23.md",
        ROOT / "docs/status/RESTRICTED_EINSTEIN_MATTER_BOOTSTRAP_PACKAGE_CERTIFICATE_2026_05_23.md",
    ]
    blob = "\n".join(p.read_text() for p in docs)
    assert "Does not prove" in blob
    assert "gravity closure" in blob
    assert "P vs NP" in blob
    assert "any Clay problem" in blob
    assert "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE" in blob
    assert "gravity solved" not in blob.lower()
