#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FloorPreservingDomainLiftSufficientCondition.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/floor_preserving_domain_lift_sufficient_condition_2026_05_18.json"
DOC = ROOT / "docs/status/FLOOR_PRESERVING_DOMAIN_LIFT_SUFFICIENT_CONDITION_2026_05_18.md"

REQUIRED_LEAN = [
    "def FloorPreservingDomainLift",
    "theorem floor_preserving_domain_lift_to_uniform_floor",
    "theorem floor_preserving_domain_lift_to_admissible_lift",
    "theorem floor_preserving_domain_lift_resolves_second_sink",
    "def FloorPreservingDomainLiftSufficientConditionStatus",
]

REQUIRED_DOC = [
    "Status: `CONDITIONAL_LIFT_SUFFICIENT_CONDITION_ONLY`",
    "Global verdict preserved: `OPEN`",
    "`FloorPreservingDomainLift`",
    "`floor_preserving_domain_lift_to_uniform_floor`",
    "`floor_preserving_domain_lift_to_admissible_lift`",
    "`floor_preserving_domain_lift_resolves_second_sink`",
    "Does not prove:",
    "unrestricted `UniversalFiberEntropyGap`",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

FORBIDDEN = [
    "P vs NP is solved",
    "Clay problem is solved",
    "unrestricted Chronos-RR is proved",
    "unrestricted H4.1/FGL is proved",
    "unrestricted UniversalFiberEntropyGap is proved",
    "existence of FloorPreservingDomainLift is proved",
    "unconditional FiniteSupportToAdmissibleDomainLift is proved",
]

def main() -> None:
    assert LEAN.exists(), f"missing Lean file: {LEAN}"
    assert ARTIFACT.exists(), f"missing artifact: {ARTIFACT}"
    assert DOC.exists(), f"missing doc: {DOC}"

    lean = LEAN.read_text()
    root_lean = ROOT_LEAN.read_text()
    artifact_text = ARTIFACT.read_text()
    doc = DOC.read_text()
    data = json.loads(artifact_text)

    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)

    for phrase in REQUIRED_LEAN:
        assert phrase in lean

    assert "import Chronos.Frontier.FloorPreservingDomainLiftSufficientCondition" in root_lean

    assert data["status"] == "CONDITIONAL_LIFT_SUFFICIENT_CONDITION_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["conditional_input"]["required_object"] == "FloorPreservingDomainLift"
    assert "floor_preserving_domain_lift_to_admissible_lift" in data["proved_surface_theorems"]
    assert "existence of FloorPreservingDomainLift" in data["boundary"]["does_not_prove"]

    for phrase in REQUIRED_DOC:
        assert phrase in doc

    combined = lean + "\n" + artifact_text + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Floor-preserving domain lift sufficient condition verified.")

if __name__ == "__main__":
    main()
