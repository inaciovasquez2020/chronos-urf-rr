#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ARTIFACT = Path(
    "artifacts/chronos/"
    "external_tensor_audit_response_required_field_negative_fixture_gate_2026_06_10.json"
)

DEPENDENCY = Path(
    "artifacts/chronos/"
    "external_tensor_audit_response_intake_negative_fixture_gate_2026_06_10.json"
)

EXPECTED_ID = "EXTERNAL_TENSOR_AUDIT_RESPONSE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE_2026_06_10"
EXPECTED_DEPENDENCY = "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_NEGATIVE_FIXTURE_GATE_2026_06_10"
EXPECTED_CLOSED_OBJECT = "ExternalTensorAuditResponseRequiredFieldNegativeFixtureGate"

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

FORBIDDEN_PROMOTION_VALUES = {
    "promoted",
    "theorem_promoted",
    "accepted_as_theorem",
    "scientific_payload_accepted",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_required_fields(fixture: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in fixture]


def main() -> None:
    data = load_json(ARTIFACT)

    assert data["id"] == EXPECTED_ID
    assert data["status"] == "verifier_only_required_field_negative_fixture_gate"
    assert data["scope"] == "external tensor audit response intake"
    assert data["closed_object"] == EXPECTED_CLOSED_OBJECT
    assert EXPECTED_DEPENDENCY in data["depends_on"]

    assert DEPENDENCY.exists(), DEPENDENCY

    required_fields = data["required_fields"]
    assert isinstance(required_fields, list)
    assert len(required_fields) == len(set(required_fields))
    assert "source_reference" in required_fields
    assert "tensor_scope" in required_fields
    assert "theorem_promotion_status" in required_fields
    assert "boundary_flags" in required_fields

    forbidden_values = set(data["forbidden_promotion_values"])
    assert FORBIDDEN_PROMOTION_VALUES <= forbidden_values

    boundary = set(data["boundary"])
    assert REQUIRED_BOUNDARY <= boundary

    fixture_path = Path(data["invalid_fixture"])
    assert fixture_path.exists(), fixture_path
    fixture = load_json(fixture_path)

    observed_missing = missing_required_fields(fixture, required_fields)
    expected_missing = data["expected_rejection"]["missing_fields"]

    assert data["expected_rejection"]["reason"] == "missing_required_fields"
    assert observed_missing == expected_missing
    assert "source_reference" in observed_missing
    assert "tensor_scope" in observed_missing

    fixture_boundary = set(fixture["boundary_flags"])
    assert REQUIRED_BOUNDARY <= fixture_boundary

    promotion_status = fixture["theorem_promotion_status"]
    assert promotion_status == "blocked"
    assert promotion_status not in forbidden_values

    assert fixture["audit_certificate_status"] == "absent"
    assert fixture["scientific_payload_status"] == "absent"

    print("EXTERNAL_TENSOR_AUDIT_RESPONSE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE_OK")


if __name__ == "__main__":
    main()
