from __future__ import annotations

import json
from pathlib import Path

from tools.verify_stl_adm_completion_lock_external_reference import verify

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/stl_adm_constraint_surface_interaction_completion_lock_external_reference_2026_06_09.json"
DOC = ROOT / "docs/status/STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_EXTERNAL_REFERENCE_2026_06_09.md"

def test_external_reference_verifies() -> None:
    verify()

def test_not_theorem_input() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "EXTERNAL_COMPLETION_LOCK_REFERENCE_ONLY_NOT_THEOREM_INPUT"
    assert data["chronos_role"] == "external_status_reference"
    assert "NOT_THEOREM_INPUT" in set(data["boundary"])

def test_source_pr_is_completion_lock() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert data["source_pr"] == 15
    assert data["source_closed_object"] == "STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_2026_06_09"

def test_no_percentage_fields() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert "stl_completion_before" not in data
    assert "stl_completion_after" not in data
    assert "%" not in ARTIFACT.read_text()
    assert "%" not in DOC.read_text()
