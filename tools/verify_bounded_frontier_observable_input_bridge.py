#!/usr/bin/env python3
from __future__ import annotations
import json
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts" / "bounded_frontier_observable_input_bridge_2026_06_23.json"
DOC = ROOT / "docs" / "status" / "BOUNDED_FRONTIER_OBSERVABLE_INPUT_BRIDGE.md"
FORBIDDEN_CLAIMS = [
"solves quantum gravity",
"quantum gravity solved",
"empirical prediction discharged",
"scientifically validated",
"completed physics theory",
"theory of everything",
"mainstream accepted",
"compilation proves physical truth",
]
REQUIRED_NON_CLAIMS = [
"does not claim quantum gravity closure",
"does not claim empirical prediction discharge",
"does not claim scientific validation",
"does not claim a completed physics theory",
"does not claim mainstream acceptance",
"does not claim that compilation proves physical truth",
]
def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def assert_no_forbidden_claims(text: str) -> None:
    lowered = text.lower()
    for required in REQUIRED_NON_CLAIMS:
        lowered = lowered.replace(required, "")
    for phrase in FORBIDDEN_CLAIMS:
        if phrase in lowered:
            raise AssertionError(f"forbidden closure claim found: {phrase}")

def assert_required_non_claims(text: str) -> None:
    lowered = text.lower()
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in lowered:
            raise AssertionError(f"missing required non-claim: {phrase}")

def assert_observation_checks(data: dict) -> None:
    tolerance = data["frontier_mapping"]["relative_tolerance"]
    if not isinstance(tolerance, (int, float)):
        raise AssertionError("relative_tolerance must be numeric")
    if tolerance <= 0 or tolerance > 0.01:
        raise AssertionError("relative_tolerance must be positive and <= 0.01")

    observations = data.get("observations")
    if not isinstance(observations, list) or not observations:
        raise AssertionError("observations must be a non-empty list")

    for obs in observations:
        label = obs.get("label", "<missing label>")
        radius = obs["radius_meters"]
        speed = obs["signal_speed_meters_per_second"]
        delta_t = obs["delta_t_seconds"]

        for name, value in [
            ("radius_meters", radius),
            ("signal_speed_meters_per_second", speed),
            ("delta_t_seconds", delta_t),
        ]:
            if not isinstance(value, (int, float)):
                raise AssertionError(f"{label}: {name} must be numeric")
            if not math.isfinite(value):
                raise AssertionError(f"{label}: {name} must be finite")

        if radius <= 0:
            raise AssertionError(f"{label}: radius_meters must be positive")
        if speed <= 0:
            raise AssertionError(f"{label}: signal_speed_meters_per_second must be positive")
        if delta_t <= 0:
            raise AssertionError(f"{label}: delta_t_seconds must be positive")

        expected = radius / speed
        relative_error = abs(delta_t - expected) / expected
        if relative_error > tolerance:
            raise AssertionError(
                f"{label}: relative error {relative_error} exceeds tolerance {tolerance}"
            )

def main() -> None:
    data = load_json(ARTIFACT)
    doc_text = DOC.read_text(encoding="utf-8")

    if data.get("status") != "BRIDGE_INPUTS_ONLY":
        raise AssertionError("status must be BRIDGE_INPUTS_ONLY")

    combined = json.dumps(data, sort_keys=True).lower() + "\n" + doc_text.lower()
    assert_no_forbidden_claims(combined)
    assert_required_non_claims(combined)
    assert_observation_checks(data)

    print("BOUNDED_FRONTIER_OBSERVABLE_INPUT_BRIDGE_OK")


if __name__ == "__main__":
    main()
