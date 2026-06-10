#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = ROOT / "schemas/chronos/external_tensor_audit_response_intake_schema_2026_06_10.json"
FIXTURE_PATH = ROOT / "fixtures/chronos/external_tensor_audit_response_missing_required_field_fixture_2026_06_10.json"
ARTIFACT_PATH = ROOT / "artifacts/chronos/external_tensor_audit_response_intake_required_field_negative_fixture_gate_2026_06_10.json"

EXPECTED_ARTIFACT_BOUNDARY = [
    "VERIFIER_ONLY",
    "SYNTHETIC_FIXTURE_ONLY",
    "NO_REQUEST_SENT",
    "NO_EXTERNAL_RESPONSE_SUPPLIED",
    "NO_AUDIT_CERTIFICATE",
    "NO_THEOREM_PROMOTION",
    "NO_NEW_SCIENTIFIC_PAYLOAD",
    "NO_OUTREACH",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def boundary_tokens(response: dict[str, Any]) -> list[str]:
    tokens = response.get("boundary_statement")
    assert isinstance(tokens, list), "boundary_statement must be a list"
    assert all(isinstance(token, str) for token in tokens), "boundary_statement tokens must be strings"
    return tokens


def rejection_reason(schema: dict[str, Any], response: dict[str, Any]) -> str | None:
    required_fields = schema["required_fields"]
    assert isinstance(required_fields, list)
    for field in required_fields:
        assert isinstance(field, str)
        if field not in response:
            return "MISSING_REQUIRED_FIELD"

    verdict = response["verdict"]
    allowed_verdicts = schema["allowed_verdicts"]
    assert isinstance(allowed_verdicts, list)
    if verdict not in allowed_verdicts:
        return "INVALID_VERDICT"

    forbidden_signals = schema["forbidden_signals"]
    assert isinstance(forbidden_signals, list)
    forbidden = set(forbidden_signals)
    if forbidden.intersection(boundary_tokens(response)):
        return "FORBIDDEN_SIGNAL_PRESENT"

    required_boundary_tokens = schema["required_boundary_tokens"]
    assert isinstance(required_boundary_tokens, list)
    missing_boundary_tokens = set(required_boundary_tokens).difference(boundary_tokens(response))
    if missing_boundary_tokens:
        return "MISSING_REQUIRED_BOUNDARY_TOKEN"

    return None


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    fixture = load_json(FIXTURE_PATH)
    artifact = load_json(ARTIFACT_PATH)

    assert artifact["id"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE_2026_06_10"
    assert artifact["date"] == "2026-06-10"
    assert artifact["repository"] == "chronos-urf-rr"
    assert artifact["status"] == "VERIFIER_ONLY"
    assert artifact["object"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE"
    assert artifact["schema"] == str(SCHEMA_PATH.relative_to(ROOT))
    assert artifact["fixture"] == str(FIXTURE_PATH.relative_to(ROOT))
    assert artifact["route"] == schema["route"]
    assert artifact["expected_rejection_reason"] == "MISSING_REQUIRED_FIELD"
    assert artifact["missing_field"] == "checked_identity"
    assert artifact["closed_object"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE"
    assert artifact["boundary"] == EXPECTED_ARTIFACT_BOUNDARY
    assert artifact["next_admissible_object"] == "STOP_OR_SCAN_NEXT_UNCONDITIONAL_BOUNDED_TARGET"

    assert fixture["response_id"] == "SYNTHETIC_MISSING_REQUIRED_FIELD_RESPONSE_FIXTURE_2026_06_10"
    assert fixture["auditor_identity"]["kind"] == "synthetic_fixture"
    assert fixture["audit_target"] == schema["id"]
    assert artifact["missing_field"] not in fixture
    assert fixture["verdict"] == "VALID"

    assert rejection_reason(schema, fixture) == artifact["expected_rejection_reason"]

    print("EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_REQUIRED_FIELD_NEGATIVE_FIXTURE_GATE_OK")


if __name__ == "__main__":
    main()
