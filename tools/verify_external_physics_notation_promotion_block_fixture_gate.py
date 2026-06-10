#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ARTIFACT = Path(
    "artifacts/chronos/"
    "external_physics_notation_promotion_block_fixture_gate_2026_06_10.json"
)

DEPENDENCY = Path(
    "artifacts/chronos/"
    "external_physics_notation_semantic_drift_audit_2026_06_10.json"
)

EXPECTED_ID = "EXTERNAL_PHYSICS_NOTATION_PROMOTION_BLOCK_FIXTURE_GATE_2026_06_10"
EXPECTED_DEPENDENCY = "EXTERNAL_PHYSICS_NOTATION_SEMANTIC_DRIFT_AUDIT_2026_06_10"
EXPECTED_CLOSED_OBJECT = "ExternalPhysicsNotationPromotionBlockFixtureGate"

REQUIRED_GATE_CONDITIONS = {
    "requires_symbol",
    "requires_domain",
    "requires_typed_meaning",
    "requires_admissibility_condition",
    "requires_source_payload_for_theorem_promotion",
    "forbids_payload_free_theorem_promotion",
}

FORBIDDEN_PROMOTION_VALUES = {
    "promoted",
    "theorem_promoted",
    "accepted_as_theorem",
    "scientific_payload_accepted",
}

REQUIRED_BOUNDARY = {
    "VERIFIER_ONLY",
    "SYNTHETIC_FIXTURE_ONLY",
    "NO_REQUEST_SENT",
    "NO_EXTERNAL_RESPONSE_SUPPLIED",
    "NO_AUDIT_CERTIFICATE",
    "NO_THEOREM_PROMOTION",
    "NO_NEW_SCIENTIFIC_PAYLOAD",
    "NO_OUTREACH",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    data = load_json(ARTIFACT)

    assert data["id"] == EXPECTED_ID
    assert data["status"] == "verifier_only_promotion_block_fixture_gate"
    assert data["scope"] == "external mathematical-physics notation theorem-promotion prevention"
    assert data["closed_object"] == EXPECTED_CLOSED_OBJECT
    assert EXPECTED_DEPENDENCY in data["depends_on"]

    assert DEPENDENCY.exists(), DEPENDENCY

    assert REQUIRED_GATE_CONDITIONS <= set(data["required_gate_conditions"])
    assert FORBIDDEN_PROMOTION_VALUES <= set(data["forbidden_promotion_values"])
    assert REQUIRED_BOUNDARY <= set(data["boundary"])

    fixture_path = Path(data["invalid_fixture"])
    assert fixture_path.exists(), fixture_path
    fixture = load_json(fixture_path)

    assert fixture["symbol"] == "t"
    assert fixture["domain"] == "High Energy Physics"
    assert fixture["typed_meaning"] == "top quark"
    assert fixture["admissibility"] == "external typed notation only"

    assert fixture["source_payload_status"] == "absent"
    assert fixture["audit_certificate_status"] == "absent"
    assert fixture["scientific_payload_status"] == "absent"

    promotion_status = fixture["theorem_promotion_status"]
    assert promotion_status in FORBIDDEN_PROMOTION_VALUES

    expected = data["expected_rejection"]
    assert expected["reason"] == "payload_free_theorem_promotion"
    assert expected["blocked_field"] == "theorem_promotion_status"
    assert expected["blocked_value"] == promotion_status

    assert REQUIRED_BOUNDARY <= set(fixture["boundary_flags"])
    assert "NO_THEOREM_PROMOTION" in fixture["boundary_flags"]

    print("EXTERNAL_PHYSICS_NOTATION_PROMOTION_BLOCK_FIXTURE_GATE_OK")


if __name__ == "__main__":
    main()
