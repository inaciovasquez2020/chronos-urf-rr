#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/external_gravity_input_values_2026_05_23.json"
LEAN = ROOT / "lean/Chronos/Frontier/ExternalGravitySourceInputValues.lean"
STATUS = ROOT / "docs/status/EXTERNAL_GRAVITY_INPUT_VALUES_2026_05_23.md"

EXPECTED_STATUS = "INPUT_VALUES_ONLY_NOT_THEOREM_INPUT"

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

def main() -> None:
    assert ARTIFACT.exists(), ARTIFACT
    assert LEAN.exists(), LEAN
    assert STATUS.exists(), STATUS

    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "EXTERNAL_GRAVITY_INPUT_VALUES_2026_05_23"
    assert data["status"] == EXPECTED_STATUS

    shadow = data["input_values"]["black_hole_shadow_lower_bound_test"]
    assert shadow["bound_ratio"] == "3*sqrt(3)/2"
    assert Fraction(shadow["bound_ratio_squared"]) == Fraction(27, 4)
    assert Fraction(shadow["test_ratio_squared"]) == Fraction(27, 4)
    assert Fraction(shadow["test_ratio_squared"]) >= Fraction(shadow["bound_ratio_squared"])
    assert shadow["gate_result"] is True

    ksz = data["input_values"]["act_ksz_inverse_square_test"]
    central = Fraction(ksz["observed_exponent_central"])
    tolerance = Fraction(ksz["observed_exponent_tolerance"])
    target = Fraction(ksz["newton_einstein_target_exponent"])
    lo, hi = map(Fraction, ksz["allowed_interval"])
    assert lo == central - tolerance
    assert hi == central + tolerance
    assert lo <= target <= hi
    assert ksz["gate_result"] is True

    finsler = data["input_values"]["finsler_friedmann_source"]
    assert finsler["numeric_gate"] is None
    assert finsler["classification"] == "ANALOGY_ONLY_NO_NUMERIC_INPUT_VALUE"

    status_text = STATUS.read_text()
    artifact_text = ARTIFACT.read_text()
    lean_text = LEAN.read_text()

    for token in REQUIRED_BOUNDARIES:
        assert token in status_text, token
        assert token in artifact_text, token

    for token in [
        "blackHoleShadowInputGate_closed",
        "actKSZInputGate_closed",
        "blackHoleShadowBoundRatioSquared",
        "actKSZObservedExponentCentral",
        "actKSZObservedExponentTolerance",
        "actKSZTargetExponent",
    ]:
        assert token in lean_text, token

    assert data["next_admissible_object"] == "PRIMARY_SOURCE_DIGEST_AND_OBSERVATIONAL_CONSTRAINT_TEST_PACKET"

    print("External gravity input values verification OK.")
    print(f"Status: {data['status']}")
    print("Input gates:")
    print("- black_hole_shadow_lower_bound_test: PASS")
    print("- act_ksz_inverse_square_test: PASS")
    print("- finsler_friedmann_source: ANALOGY_ONLY_NO_NUMERIC_GATE")

if __name__ == "__main__":
    main()
