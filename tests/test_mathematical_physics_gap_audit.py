from __future__ import annotations

import subprocess


def test_mathematical_physics_gap_audit_verifier() -> None:
    result = subprocess.run(
        ["python3", "tools/verify_mathematical_physics_gap_audit.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "MATHEMATICAL_PHYSICS_GAP_AUDIT_OK" in result.stdout
