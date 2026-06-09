from __future__ import annotations

import json
from pathlib import Path

from tools.verify_stl_adm_formal_model_external_reference import verify

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/stl_adm_constraint_surface_interaction_formal_model_external_reference_2026_06_09.json"

def test_external_reference_verifies() -> None:
    verify()

def test_not_theorem_input() -> None:
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "EXTERNAL_STATUS_REFERENCE_ONLY_NOT_THEOREM_INPUT"
    assert data["chronos_role"] == "external_status_reference"
    assert "NOT_THEOREM_INPUT" in set(data["boundary"])

def test_no_completion_percentage_fields() -> None:
    text = ARTIFACT.read_text()
    assert "completion" not in text.lower()
    assert "%" not in text
