from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_payload_field_proof_payloads_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_restricted_continuation_norm_control_payload_field_proof_payloads.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verifier OK" in result.stdout
    assert "CONDITIONAL_PAYLOAD_FIELD_PROOF_PAYLOADS" in result.stdout
    assert "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT" in result.stdout

def test_restricted_continuation_norm_control_payload_field_proof_payloads_boundary() -> None:
    text = (ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_PAYLOAD_FIELD_PROOF_PAYLOADS_2026_06_13.md").read_text()
    assert "conditional payload field proof payload surface" in text
    assert "does not derive those payloads from PDE equations" in text
    assert "STOP_AFTER_THIS_COMMIT_NO_ADMISSIBLE_NEXT_STEP_WITHOUT_NEW_ANALYTIC_INPUT" in text
