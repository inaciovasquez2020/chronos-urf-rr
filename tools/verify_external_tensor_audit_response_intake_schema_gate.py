#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/chronos/external_tensor_audit_response_intake_schema_2026_06_10.json"
ARTIFACT_PATH = ROOT / "artifacts/chronos/external_tensor_audit_response_intake_schema_gate_2026_06_10.json"

EXPECTED_REQUIRED_FIELDS = [
    "response_id",
    "auditor_identity",
    "audit_target",
    "checked_identity",
    "verdict",
    "defects_found",
    "corrections_required",
    "boundary_statement",
    "attachments",
]

EXPECTED_ALLOWED_VERDICTS = [
    "VALID",
    "VALID_WITH_CORRECTIONS",
    "INVALID",
    "INSUFFICIENT_INFORMATION",
]

EXPECTED_REQUIRED_BOUNDARY_TOKENS = [
    "NO_RESPONSE_SUPPLIED",
    "NO_AUDIT_CERTIFICATE",
    "NO_THEOREM_PROMOTION",
    "NO_NEW_SCIENTIFIC_PAYLOAD",
    "NO_OUTREACH",
]

EXPECTED_FORBIDDEN_SIGNALS = [
    "REQUEST_SENT",
    "RESPONSE_SUPPLIED",
    "AUDIT_CERTIFICATE_SUPPLIED",
    "POSITIVE_AUDIT_CERTIFICATE",
    "THEOREM_PROMOTION",
    "SCIENTIFIC_CLOSURE",
    "P_VS_NP_CLAIM",
    "CLAY_CLAIM",
]

EXPECTED_ARTIFACT_BOUNDARY = [
    "VERIFIER_ONLY",
    "NO_REQUEST_SENT",
    "NO_RESPONSE_SUPPLIED",
    "NO_AUDIT_CERTIFICATE",
    "NO_THEOREM_PROMOTION",
    "NO_NEW_SCIENTIFIC_PAYLOAD",
    "NO_OUTREACH",
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def main() -> None:
    schema = load_json(SCHEMA_PATH)
    artifact = load_json(ARTIFACT_PATH)

    assert schema["id"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA"
    assert schema["date"] == "2026-06-10"
    assert schema["repository"] == "chronos-urf-rr"
    assert schema["kind"] == "audit_response_intake_schema"
    assert schema["route"] == "ROUTE_B_EXTERNAL_TENSOR_AUDIT"
    assert schema["required_fields"] == EXPECTED_REQUIRED_FIELDS
    assert schema["allowed_verdicts"] == EXPECTED_ALLOWED_VERDICTS
    assert schema["required_boundary_tokens"] == EXPECTED_REQUIRED_BOUNDARY_TOKENS
    assert schema["forbidden_signals"] == EXPECTED_FORBIDDEN_SIGNALS

    assert artifact["id"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA_GATE_2026_06_10"
    assert artifact["date"] == "2026-06-10"
    assert artifact["repository"] == "chronos-urf-rr"
    assert artifact["status"] == "VERIFIER_ONLY"
    assert artifact["object"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA_GATE"
    assert artifact["schema"] == str(SCHEMA_PATH.relative_to(ROOT))
    assert artifact["route"] == schema["route"]
    assert artifact["closed_object"] == "EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA_GATE"
    assert artifact["boundary"] == EXPECTED_ARTIFACT_BOUNDARY
    assert artifact["next_admissible_object"] == "STOP_OR_SCAN_NEXT_UNCONDITIONAL_BOUNDED_TARGET"

    assert "NO_REQUEST_SENT" not in schema["required_boundary_tokens"]
    assert "REQUEST_SENT" in schema["forbidden_signals"]
    assert "RESPONSE_SUPPLIED" in schema["forbidden_signals"]
    assert "AUDIT_CERTIFICATE_SUPPLIED" in schema["forbidden_signals"]

    print("EXTERNAL_TENSOR_AUDIT_RESPONSE_INTAKE_SCHEMA_GATE_OK")


if __name__ == "__main__":
    main()
