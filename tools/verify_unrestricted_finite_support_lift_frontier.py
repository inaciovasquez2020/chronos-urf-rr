#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/UnrestrictedFiniteSupportLiftFrontier.lean"
ROOT_LEAN = ROOT / "lean/Chronos.lean"
ARTIFACT = ROOT / "artifacts/chronos/unrestricted_finite_support_lift_frontier_2026_05_18.json"
DOC = ROOT / "docs/status/UNRESTRICTED_FINITE_SUPPORT_LIFT_FRONTIER_2026_05_18.md"

def main() -> None:
    lean = LEAN.read_text()
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    root = ROOT_LEAN.read_text()

    assert not re.search(r"\b(sorry|admit|axiom)\b", lean)
    assert "def UnrestrictedFiniteSupportToAdmissibleDomainLift" in lean
    assert "def UnrestrictedFiniteSupportLiftFailureCountermodel" in lean
    assert "theorem unrestricted_lift_failure_countermodel_excludes_unrestricted_lift" in lean
    assert "import Chronos.Frontier.UnrestrictedFiniteSupportLiftFrontier" in root

    assert data["status"] == "UNRESTRICTED_LIFT_FRONTIER_OPEN"
    assert data["global_verdict_preserved"] == "OPEN"
    assert data["claim_promotion"] is False
    assert data["weakest_missing_lemma"] == "UnrestrictedFiniteSupportToAdmissibleDomainLift"

    for phrase in [
        "Status: `UNRESTRICTED_LIFT_FRONTIER_OPEN`",
        "Does not prove:",
        "unrestricted `UniversalFiberEntropyGap`",
        "unrestricted Chronos-RR",
        "unrestricted H4.1/FGL",
        "P vs NP",
        "any Clay problem",
    ]:
        assert phrase in doc

    combined = lean + "\n" + json.dumps(data) + "\n" + doc
    for phrase in [
        "P vs NP is solved",
        "Clay problem is solved",
        "unrestricted Chronos-RR is proved",
        "unrestricted UniversalFiberEntropyGap is proved",
        "UnrestrictedFiniteSupportToAdmissibleDomainLift is proved",
    ]:
        assert phrase not in combined

    print("Unrestricted finite-support lift frontier verified.")

if __name__ == "__main__":
    main()
