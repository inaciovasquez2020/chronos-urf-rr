from __future__ import annotations

import subprocess


def test_external_physics_notation_semantic_drift_audit_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_external_physics_notation_semantic_drift_audit.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "EXTERNAL_PHYSICS_NOTATION_SEMANTIC_DRIFT_AUDIT_OK" in result.stdout
