#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportToAdmissibleDomainLiftTarget.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/finite_support_to_admissible_domain_lift_target_2026_05_18.json"
DOC = ROOT / "docs/status/FINITE_SUPPORT_TO_ADMISSIBLE_DOMAIN_LIFT_TARGET_2026_05_18.md"

REQUIRED_LEAN = [
    "def FiniteSupportToAdmissibleDomainLift",
    "def FiniteSupportLiftFailureCountermodel",
    "theorem finite_support_lift_transfers_floor",
    "theorem finite_support_lift_resolves_admissible_sink",
    "theorem finite_support_lift_failure_countermodel_excludes_lift",
    "def FiniteSupportToAdmissibleDomainLiftTargetStatus",
]

REQUIRED_DOC = [
    "Status: `OPEN_LIFT_TARGET_SURFACE_ONLY`",
    "Global verdict preserved: `OPEN`",
    "`FiniteSupportToAdmissibleDomainLift`",
    "`FiniteSupportLiftFailureCountermodel`",
    "`finite_support_lift_failure_countermodel_excludes_lift`",
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
    "existence of FiniteSupportToAdmissibleDomainLift is proved",
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

    assert "import Chronos.Frontier.FiniteSupportToAdmissibleDomainLiftTarget" in root_lean

    assert data["status"] == "OPEN_LIFT_TARGET_SURFACE_ONLY"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["sink_id"] == "domain_lift_from_finite_support"
    assert "finite_support_lift_failure_countermodel_excludes_lift" in data["proved_surface_theorems"]
    assert "existence of FiniteSupportToAdmissibleDomainLift" in data["boundary"]["does_not_prove"]

    for phrase in REQUIRED_DOC:
        assert phrase in doc

    combined = lean + "\n" + artifact_text + "\n" + doc
    for phrase in FORBIDDEN:
        assert phrase not in combined

    print("Finite-support to admissible-domain lift target verified.")

if __name__ == "__main__":
    main()
