from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_external_tensor_audit_request_template_verifier() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "tools/verify_external_tensor_audit_request_template.py"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "EXTERNAL_TENSOR_AUDIT_REQUEST_TEMPLATE_OK" in result.stdout
    assert "BOUNDARY=REQUEST_TEMPLATE_SCHEMA_VERIFIER_ONLY_NO_REQUEST_SENT" in result.stdout
