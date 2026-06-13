from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_payload_field_analytic_proofs_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_payload_field_analytic_proofs.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_PAYLOAD_FIELD_ANALYTIC_PROOFS" in result.stdout

def test_restricted_continuation_norm_control_payload_field_analytic_proofs_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_ANALYTIC_PROOFS_2026_06_13.md").read_text()
    assert "conditional payload field analytic proofs surface" in text
    assert "does not derive the payload field proof payloads" in text
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_PROOF_PAYLOADS" in text
