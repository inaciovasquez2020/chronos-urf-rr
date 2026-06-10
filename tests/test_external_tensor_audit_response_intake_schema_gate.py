from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_external_tensor_audit_response_intake_schema_gate_verifier() -> None:
    result = subprocess.run(
        [sys.executable, "tools/verify_external_tensor_audit_response_intake_schema_gate.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA_GATE_OK" in result.stdout
