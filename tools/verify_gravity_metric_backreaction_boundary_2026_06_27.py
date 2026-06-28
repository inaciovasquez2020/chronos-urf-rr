#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts/external_validation/gravity_metric_backreaction_boundary_2026_06_27.json"

EXPECTED_RANKED_GAPS = [
    "emergent metric/backreaction construction",
    "Einstein-limit derivation obligation",
    "quantitative prediction interface",
    "separation from GR plus scalar fields",
]

EXPECTED_NOT_CLAIMED = [
    "derivation of gravitational field equations",
    "Einstein-equation recovery",
    "metric backreaction theorem",
    "new gravitational prediction",
    "solution of gravity",
]


def main() -> None:
    if not TARGET.is_file():
        raise SystemExit(f"MISSING_OBJECT := {TARGET.relative_to(ROOT)}")

    data = json.loads(TARGET.read_text())

    checks = {
        "object": "GRAVITY_METRIC_BACKREACTION_BOUNDARY_2026_06_27",
        "repository": "chronos-urf-rr",
        "status": "boundary_not_solution",
    }

    for key, expected in checks.items():
        if data.get(key) != expected:
            raise SystemExit(f"MISSING_OBJECT := {key} == {expected}")

    boundary = data.get("boundary", "")
    for phrase in [
        "no current verifier-backed object",
        "derives metric backreaction",
        "recovers the Einstein limit",
        "quantitative gravitational prediction",
    ]:
        if phrase not in boundary:
            raise SystemExit(f"MISSING_OBJECT := boundary phrase {phrase}")

    if data.get("ranked_gaps") != EXPECTED_RANKED_GAPS:
        raise SystemExit("MISSING_OBJECT := ranked_gaps exact gravity backreaction boundary list")

    if data.get("not_claimed") != EXPECTED_NOT_CLAIMED:
        raise SystemExit("MISSING_OBJECT := not_claimed exact gravity non-claim list")

    print("GRAVITY_METRIC_BACKREACTION_BOUNDARY_2026_06_27_OK")


if __name__ == "__main__":
    main()
