#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "chronos" / "terminal_admissible_boundary_chain_certificate_2026_05_18.json"

EXPECTED_STATUS = "TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_CLOSED_NO_THEOREM_PROMOTION"
EXPECTED_RESULT = "TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_OK"

FORBIDDEN_PROMOTION_SIGNALS = {
    "THEOREM_PROMOTED",
    "THEOREM_PROMOTION_SUPPLIED",
    "PROMOTED_TO_THEOREM",
    "FINAL_THEOREM_CLOSED",
    "SCIENTIFIC_CLOSURE",
    "P_VS_NP_CLAIM",
    "CLAY_CLAIM",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"TERMINAL_ADMISSIBLE_BOUNDARY_CHAIN_CERTIFICATE_FAIL: {message}")


def walk_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        out: list[str] = []
        for key, item in value.items():
            out.append(str(key))
            out.extend(walk_values(item))
        return out
    if isinstance(value, list):
        out = []
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

    for signal in FORBIDDEN_PROMOTION_SIGNALS:
        require(signal not in serialized_values, f"forbidden promotion signal present: {signal}")

    require("NO_THEOREM_PROMOTION" in serialized_values, "missing no-theorem-promotion boundary")

    print(EXPECTED_RESULT)
    print(f"STATUS={EXPECTED_STATUS}")
    print("BOUNDARY=CLOSED_NO_THEOREM_PROMOTION_VERIFIER_ONLY")


if __name__ == "__main__":
    main()
