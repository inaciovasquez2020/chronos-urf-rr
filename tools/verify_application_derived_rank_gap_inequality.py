#!/usr/bin/env python3
import json
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/ApplicationDerivedRankGapInequality.lean")
ART = Path("artifacts/chronos/application_derived_rank_gap_inequality_2026_05_27.json")
DOC = Path("docs/status/APPLICATION_DERIVED_RANK_GAP_INEQUALITY_2026_05_27.md")
ROOT = Path("lean/Chronos.lean")

for path in [LEAN, ART, DOC, ROOT]:
    assert path.exists(), f"missing required file: {path}"

src = LEAN.read_text()
artifact_text = ART.read_text()
doc_text = DOC.read_text()
root_text = ROOT.read_text()
data = json.loads(artifact_text)

required_src_tokens = [
    "ApplicationDerivedRankGapInequality",
    "applicationName",
    "semanticRankRate",
    "fiberEntropyGap",
    "slack",
    "nontrivialSlack",
    "rankToGapInequality",
    "finiteRegisteredHyperbolicApplicationRankGapInequality",
    "finiteRegisteredHyperbolicApplication_rank_lt_gap",
    "finiteRegisteredHyperbolicApplication_has_nontrivial_slack",
    "finiteRegisteredHyperbolicApplication_rank_plus_slack_le_gap",
]

required_artifact_tokens = [
    "APPLICATION_DERIVED_RANK_GAP_INEQUALITY_CLOSED_ONE_STACK_TARGET_ONLY",
    "applicationDerivedRankGapInequality",
    "replace toy numeric application-derived inequality with a proof extracted from the concrete non-toy target application data",
]

required_doc_tokens = [
    "APPLICATION_DERIVED_RANK_GAP_INEQUALITY_CLOSED_ONE_STACK_TARGET_ONLY",
    "ApplicationDerivedRankGapInequality",
    "Does not prove",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "P vs NP",
    "any Clay problem",
]

for token in required_src_tokens:
    assert token in src, token

for token in required_artifact_tokens:
    assert token in artifact_text, token

for token in required_doc_tokens:
    assert token in doc_text, token

assert "import Chronos.Frontier.ApplicationDerivedRankGapInequality" in root_text

assert data["status"] == "APPLICATION_DERIVED_RANK_GAP_INEQUALITY_CLOSED_ONE_STACK_TARGET_ONLY"
assert data["object"] == "applicationDerivedRankGapInequality"
assert data["semantic_rank_rate"] + data["slack"] <= data["fiber_entropy_gap"]
assert data["slack"] > 0

for forbidden in [
    "proves UniversalFiberEntropyGap",
    "proves Chronos-RR",
    "proves P vs NP",
    "proves any Clay problem",
]:
    assert forbidden not in src
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("APPLICATION_DERIVED_RANK_GAP_INEQUALITY_OK")
print(json.dumps({
    "object": data["object"],
    "status": data["status"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
