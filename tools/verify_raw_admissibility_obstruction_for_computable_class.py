#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/RawAdmissibilityObstructionForComputableClass.lean"
ART = ROOT / "artifacts/chronos/raw_admissibility_obstruction_for_computable_class_2026_05_27.json"
DOC = ROOT / "docs/status/RAW_ADMISSIBILITY_OBSTRUCTION_FOR_COMPUTABLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "import Chronos.Frontier.StructuredAdmissibilityDominanceForComputableClass",
    "def rawAdmissibilityCounterexample",
    "semanticRankRate := 1",
    "fiberEntropyGap := 0",
    "admissible := True",
    "theorem raw_admissibility_counterexample_no_bridge",
    "theorem not_raw_to_structured_admissibility_dominance",
    "theorem not_finite_support_bridge_law_for_computable_class",
    "theorem not_finite_support_bridge_certificate_supply",
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.RawAdmissibilityObstructionForComputableClass" in root_import
assert data["status"] == "RAW_ADMISSIBILITY_OBSTRUCTION_PROVED"
assert data["object"] == "rawAdmissibilityCounterexample"
assert data["counterexample"]["semanticRankRate"] == 1
assert data["counterexample"]["fiberEntropyGap"] == 0
assert data["counterexample"]["admissible"] is True

for boundary in [
    "structured admissibility for raw objects",
    "intrinsic bridge from opaque raw admissibility",
    "stability under admissible limits",
    "finite-support approximation theorem",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]:
    assert boundary in data["does_not_prove"], boundary
    assert boundary in doc, boundary

assert "RAW_ADMISSIBILITY_OBSTRUCTION_PROVED" in doc
assert "¬ RawToStructuredAdmissibilityDominance" in doc

print("RAW_ADMISSIBILITY_OBSTRUCTION_FOR_COMPUTABLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
