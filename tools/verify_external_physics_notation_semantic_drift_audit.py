#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ARTIFACT = Path("artifacts/chronos/external_physics_notation_semantic_drift_audit_2026_06_10.json")
EXPECTED_ID = "EXTERNAL_PHYSICS_NOTATION_SEMANTIC_DRIFT_AUDIT_2026_06_10"
EXPECTED_CLOSED_OBJECT = "ExternalPhysicsNotationSemanticDriftAudit"

REQUIRED_DEPENDENCIES = {
    "HEP_T_EXTERNAL_NOTATION_CLASSIFICATION_2026_06_10",
    "MATHEMATICAL_PHYSICS_GAP_AUDIT_2026_06_10",
}

REQUIRED_AUDIT_CLASSES = {
    "symbol_collision",
    "type_drift",
    "domain_drift",
    "theorem_promotion_drift",
    "abstraction_elevation",
}

REQUIRED_EXCLUSIONS = {
    "new physics theorem",
    "new mathematical-physics proof",
    "QFT phenomenology expansion",
    "scattering-amplitude theorem",
    "top-quark theorem",
    "Yang-Mills mass-gap proof",
    "cosmic-censorship proof",
}

DEPENDENCY_FILES = [
    Path("artifacts/chronos/hep_t_external_notation_classification_2026_06_10.json"),
    Path("artifacts/chronos/mathematical_physics_gap_audit_2026_06_10.json"),
]


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    assert data["id"] == EXPECTED_ID
    assert data["status"] == "notation_semantic_drift_audit_only"
    assert data["scope"] == "external mathematical-physics notation"
    assert data["closed_object"] == EXPECTED_CLOSED_OBJECT

    for dependency_file in DEPENDENCY_FILES:
        assert dependency_file.exists(), dependency_file

    assert REQUIRED_DEPENDENCIES <= set(data["depends_on"])

    audit_classes = {entry["class"] for entry in data["audit_classes"]}
    assert REQUIRED_AUDIT_CLASSES == audit_classes

    for entry in data["audit_classes"]:
        assert entry["description"]
        assert entry["required_record"]
        assert all(isinstance(item, str) and item for item in entry["required_record"])

    cases = data["canonical_cases"]
    assert len(cases) == 3

    case_index = {
        (case["symbol"], case["domain"], case["typed_meaning"]): case
        for case in cases
    }

    assert ("t", "High Energy Physics", "top quark") in case_index
    assert ("t", "scattering theory", "Mandelstam momentum-transfer variable") in case_index
    assert ("t", "GR/PDE evolution", "time or evolution parameter") in case_index

    for case in cases:
        assert case["core_unification_primitive"] is False
        assert case["core_theorem_target"] is False
        assert "notation" in case["admissibility"] or "payload" in case["admissibility"]

    gate = data["admissibility_gate"]
    assert gate["requires_symbol"] is True
    assert gate["requires_domain"] is True
    assert gate["requires_typed_meaning"] is True
    assert gate["requires_admissibility_condition"] is True
    assert gate["requires_source_payload_for_theorem_promotion"] is True
    assert gate["forbids_untyped_symbol_reuse"] is True
    assert gate["forbids_domain_free_import"] is True
    assert gate["forbids_payload_free_theorem_promotion"] is True

    assert REQUIRED_EXCLUSIONS <= set(data["excluded_outputs"])

    boundary = data["boundary"]
    assert "semantic-drift control surface" in boundary
    assert "no new physics theorem" in boundary
    assert "no scientific payload" in boundary
    assert "no theorem promotion" in boundary

    print("EXTERNAL_PHYSICS_NOTATION_SEMANTIC_DRIFT_AUDIT_OK")


if __name__ == "__main__":
    main()
