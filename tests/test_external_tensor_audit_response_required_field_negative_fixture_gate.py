from __future__ import annotations

import subprocess


def test_external_tensor_audit_response_required_field_negative_fixture_gate_verifier() -> None:
    result = subprocess.run(
        [
            "python3",
            "tools/verify_external_tensor_audit_response_required_field_negative_fixture_gate.py",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert (
        "EXTERNAL_TENSOR_AUDIT_RESPONSE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE_OK"
        in result.stdout
    )
