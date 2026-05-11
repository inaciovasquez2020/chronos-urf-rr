from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_native_zero_arity_interface_audit_generates_latest() -> None:
    completed = subprocess.run(
        [sys.executable, "tools/audit_repository_native_zero_arity_interface.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["status"] == "FRONTIER_OPEN / ACTIVE_NATIVE_INTERFACE_AUDIT_ONLY"
    assert payload["theorem_level_closure"] is False
    assert isinstance(payload["missing_fields"], list)
    assert isinstance(payload["candidate_files"], dict)


def test_repository_native_zero_arity_interface_audit_verifier_passes() -> None:
    latest = subprocess.run(
        [sys.executable, "tools/audit_repository_native_zero_arity_interface.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    (ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_latest.json").write_text(
        latest.stdout
    )

    subprocess.run(
        [sys.executable, "tools/verify_repository_native_zero_arity_interface_audit.py"],
        cwd=ROOT,
        check=True,
    )
