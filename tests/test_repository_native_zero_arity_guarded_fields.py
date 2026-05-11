from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_repository_native_zero_arity_guarded_fields_verifier_passes() -> None:
    audit = subprocess.run(
        [sys.executable, "tools/audit_repository_native_zero_arity_interface.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    (ROOT / "artifacts/chronos/repository_native_zero_arity_interface_audit_latest.json").write_text(
        audit.stdout
    )

    subprocess.run(
        [sys.executable, "tools/verify_repository_native_zero_arity_guarded_fields.py"],
        cwd=ROOT,
        check=True,
    )


def test_repository_native_zero_arity_guarded_fields_artifact_boundary() -> None:
    payload = json.loads(
        (ROOT / "artifacts/chronos/repository_native_zero_arity_guarded_fields_2026_05_11.json").read_text()
    )

    assert payload["status"] == "FRONTIER_OPEN / GUARDED_INTERFACE_FIELDS_ONLY"
    assert payload["theorem_level_closure"] is False
    assert payload["active_native_instantiation"] is False
    assert payload["unrestricted_chronos_rr_closure"] is False
    assert payload["h4_1_fgl_closure"] is False
    assert payload["universal_fiber_entropy_gap_closure"] is False
    assert payload["p_vs_np_closure"] is False
    assert payload["clay_problem_closure"] is False
    assert len(payload["guarded_missing_fields"]) == 8
