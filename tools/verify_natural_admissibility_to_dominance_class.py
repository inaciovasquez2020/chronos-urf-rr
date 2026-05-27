#!/usr/bin/env python3
import json
import re
from pathlib import Path

LEAN = Path("lean/Chronos/Frontier/NaturalAdmissibilityToDominanceClass.lean")
ART = Path("artifacts/chronos/natural_admissibility_to_dominance_class_2026_05_27.json")
DOC = Path("docs/status/NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_2026_05_27.md")

src = LEAN.read_text()
data = json.loads(ART.read_text())
doc = DOC.read_text()

required_src_tokens = [
    "NaturalAdmissibilityDominanceCertificate",
    "NaturalDominanceAdmissibleComputableClass",
    "DominanceAdmissibleComputableClass",
]

for token in required_src_tokens:
    assert token in src, token

assert re.search(
    r"SemanticRankRate\s+X\s*(?:<=|≤)\s*FiberEntropyGap\s+X",
    src,
), "SemanticRankRate X <= FiberEntropyGap X"

assert data["status"] == "NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_INTERFACE"
assert data["object"] == "NaturalDominanceAdmissibleComputableClass"
assert data["next_missing_ingredient"] == (
    "construct NaturalAdmissibilityDominanceCertificate inside each target application"
)

required_boundaries = [
    "certificate construction for any target application",
    "raw opaque admissibility implies dominance",
    "RawToStructuredAdmissibilityDominance for the old raw class",
    "stability under admissible limits",
    "finite-support approximation theorem",
    "unrestricted semantic-rank-to-fiber-entropy bridge",
    "UniversalFiberEntropyGap",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for boundary in required_boundaries:
    assert boundary in data["does_not_prove"], boundary
    assert boundary in doc, boundary

assert "NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_INTERFACE" in doc
assert "NaturalAdmissibilityDominanceCertificate" in doc

print("NATURAL_ADMISSIBILITY_TO_DOMINANCE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
