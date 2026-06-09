from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/stl_adm_constraint_surface_interaction_completion_lock_external_reference_2026_06_09.json"
DOC = ROOT / "docs/status/STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_EXTERNAL_REFERENCE_2026_06_09.md"

EXPECTED_BOUNDARY = {
    "EXTERNAL_REFERENCE_ONLY",
    "NOT_THEOREM_INPUT",
    "NO_CHRONOS_RR_CLOSURE",
    "NO_H4_1_FGL_CLOSURE",
    "NO_QUANTUM_GRAVITY_CLAIM",
    "NO_CANONICAL_QUANTIZATION_CLAIM",
    "NO_EINSTEIN_EQUATION_CLAIM",
    "NO_EMPIRICAL_GRAVITY_CLAIM",
    "NO_COSMOLOGY_CLAIM",
    "NO_UNIFICATION_CLAIM",
    "NO_PHYSICAL_THEORY_CLAIM",
    "NO_SOLUTION_OF_GRAVITY_CLAIM",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM",
}

FORBIDDEN_KEYS = {
    "stl_completion_before",
    "stl_completion_after",
    "completion_before",
    "completion_after",
}

def verify() -> None:
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["object"] == "STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_EXTERNAL_REFERENCE_2026_06_09"
    assert data["status"] == "EXTERNAL_COMPLETION_LOCK_REFERENCE_ONLY_NOT_THEOREM_INPUT"
    assert data["source_repository"] == "inaciovasquez2020/theorem-closure-classifier"
    assert data["source_pr"] == 15
    assert data["source_closed_object"] == "STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_2026_06_09"
    assert data["source_status"] == "STL_ADM_CONSTRAINT_SURFACE_INTERACTION_COMPLETION_LOCK_ONLY"
    assert data["chronos_role"] == "external_status_reference"
    assert data["minimal_missing_object"] == "STOP_OR_EXTERNAL_REFERENCE_SYNC"
    assert set(data["boundary"]) == EXPECTED_BOUNDARY
    assert data["next_admissible_object"] == "STOP"
    assert not (FORBIDDEN_KEYS & set(data))
    assert "%" not in ARTIFACT.read_text()
    assert "%" not in doc

    for token in [
        data["object"],
        data["status"],
        data["source_repository"],
        data["source_closed_object"],
        data["source_status"],
        data["minimal_missing_object"],
        data["next_admissible_object"],
        *EXPECTED_BOUNDARY,
    ]:
        assert str(token) in doc

if __name__ == "__main__":
    verify()
    print("STL_ADM_COMPLETION_LOCK_EXTERNAL_REFERENCE_OK")
