#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "chronos" / "external_tensor_audit_request_template_2026_05_22.json"

EXPECTED_STATUS = "REQUEST_TEMPLATE_SCHEMA_RECORDED_NO_REQUEST_SENT"
EXPECTED_RESULT = "EXTERNAL_TENSOR_AUDIT_REQUEST_TEMPLATE_OK"

FORBIDDEN_SIGNALS = {
    "REQUEST_SENT",
    "RESPONSE_SUPPLIED",
    "AUDIT_CERTIFICATE_SUPPLIED",
    "POSITIVE_AUDIT_CERTIFICATE",
    "THEOREM_PROMOTION",
    "SCIENTIFIC_CLOSURE",
    "P_VS_NP_CLAIM",
    "CLAY_CLAIM",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"EXTERNAL_TENSOR_AUDIT_REQUEST_TEMPLATE_FAIL: {message}")


def walk_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for key, item in value.items():
            out.append(str(key))
            out.extend(walk_values(item))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(walk_values(item))
        return out
    return [str(value)]


def main() -> None:
    require(ARTIFACT.exists(), f"missing artifact: {ARTIFACT}")

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "artifact root must be a JSON object")
    require(data.get("status") == EXPECTED_STATUS, f"unexpected status: {data.get('status')!r}")

    serialized_values = "\n".join(walk_values(data)).upper()

    require("NO_REQUEST_SENT" in serialized_values, "missing no-request-sent boundary")

    for signal in FORBIDDEN_SIGNALS:
        if signal == "REQUEST_SENT":
            require("NO_REQUEST_SENT" in serialized_values, "missing no-request-sent guard")
            continue
        require(signal not in serialized_values, f"forbidden signal present: {signal}")

    print(EXPECTED_RESULT)
    print(f"STATUS={EXPECTED_STATUS}")
    print("BOUNDARY=REQUEST_TEMPLATE_SCHEMA_VERIFIER_ONLY_NO_REQUEST_SENT")


if __name__ == "__main__":
    main()
