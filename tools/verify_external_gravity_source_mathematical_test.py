#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/external_gravity_source_mathematical_test_2026_05_23.json"
LEAN = ROOT / "lean/Chronos/Frontier/ExternalGravitySourceMathematicalTest.lean"
STATUS = ROOT / "docs/status/EXTERNAL_GRAVITY_SOURCE_MATHEMATICAL_TEST_2026_05_23.md"

EXPECTED_STATUS = "SOURCE_BACKED_MATHEMATICAL_TEST_ONLY_NOT_THEOREM_INPUT"

REQUIRED_BOUNDARIES = [
    "Does not prove gravity closure",
    "Does not prove physical Einstein-matter flux identity",
    "Does not prove restricted analytic estimate assumption",
    "Does not prove dark matter detection",
    "Does not prove dark energy disproof",
    "Does not prove DFM-MKC validation",
    "Does not prove Lambda-CDM failure",
    "Does not prove Chronos-RR",
    "Does not prove H4.1/FGL",
    "Does not prove P vs NP",
    "Does not prove any Clay problem",
]

REQUIRED_SOURCE_IDS = {
    "APS_PRD_BLACK_HOLE_SHADOW_LOWER_BOUND",
    "ACT_KSZ_INVERSE_SQUARE_GRAVITY_CONSTRAINT",
    "FINSLER_FRIEDMANN_GEOMETRIC_ACCELERATION_ANALOGY",
}

def load() -> dict:
    return json.loads(ARTIFACT.read_text())

def main() -> None:
    assert ARTIFACT.exists(), ARTIFACT
    assert LEAN.exists(), LEAN
    assert STATUS.exists(), STATUS

    data = load()
    assert data["status"] == EXPECTED_STATUS

    source_ids = {entry["source_id"] for entry in data["sources"]}
    assert REQUIRED_SOURCE_IDS <= source_ids

    urls = "\n".join(entry["source_url"] for entry in data["sources"])
    assert "journals.aps.org/prd/abstract/10.1103/83t3-r7j2" in urls
    assert "okdiario.com/techy/en/einstein-and-newton" in urls
    assert "sciencedaily.com/releases/2026/01/260110211221.htm" in urls

    tests = {entry["name"]: entry for entry in data["mathematical_tests"]}
    assert tests["black_hole_shadow_lower_bound_squared_gate"]["passes"] is True
    assert Fraction(tests["black_hole_shadow_lower_bound_squared_gate"]["test_value"]) == Fraction(27, 4)

    ksz = tests["act_ksz_inverse_square_one_sigma_gate"]
    central = Fraction(ksz["central"])
    tolerance = Fraction(ksz["tolerance"])
    target = Fraction(ksz["target"])
    assert central - tolerance <= target <= central + tolerance
    assert ksz["passes"] is True

    text = STATUS.read_text()
    lean = LEAN.read_text()
    artifact_text = ARTIFACT.read_text()

    for token in REQUIRED_BOUNDARIES:
        assert token in text, token
        assert token in artifact_text, token

    assert "blackHoleShadowSquaredLowerBound" in lean
    assert "actKSZInverseSquareMathGate_closed" in lean
    assert "blackHoleShadowLowerBoundSaturationGate_closed" in lean
    assert data["next_admissible_object"] == "PRIMARY_SOURCE_DIGEST_AND_OBSERVATIONAL_CONSTRAINT_TEST_PACKET"

    print("External gravity source mathematical test verification OK.")
    print(f"Status: {data['status']}")
    print("Mathematical gates:")
    for item in data["mathematical_tests"]:
        print(f"- {item['name']}: PASS")

if __name__ == "__main__":
    main()
