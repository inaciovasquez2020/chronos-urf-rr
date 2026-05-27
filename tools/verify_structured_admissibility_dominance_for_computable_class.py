#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/StructuredAdmissibilityDominanceForComputableClass.lean"
ART = ROOT / "artifacts/chronos/structured_admissibility_dominance_for_computable_class_2026_05_27.json"
DOC = ROOT / "docs/status/STRUCTURED_ADMISSIBILITY_DOMINANCE_FOR_COMPUTABLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "import Chronos.Frontier.CertificateSupplyLawForComputableClass",
    "structure StructuredAdmissibilityDominance",
    "rank_entropy_dominance",
    "theorem structured_admissibility_supplies_bridge",
    "def StructuredFiniteSupportBridgeLaw : Prop",
    "theorem structured_finite_support_bridge_law",
    "def RawToStructuredAdmissibilityDominance : Prop",
    "theorem finite_support_bridge_law_from_raw_to_structured",
    "theorem certificate_supply_from_raw_to_structured",
    "def RawToStructuredAdmissibilityDominanceProblem : Prop",
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.StructuredAdmissibilityDominanceForComputableClass" in root_import
assert data["status"] == "STRUCTURED_ADMISSIBILITY_DOMINANCE_ONLY"
assert data["structural_action"] == 4
assert data["object"] == "StructuredAdmissibilityDominance"

for boundary in [
    "RawToStructuredAdmissibilityDominance",
    "intrinsic finite-support bridge law from opaque raw admissibility alone",
    "certificate supply theorem without structured dominance or explicit law",
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

assert "STRUCTURED_ADMISSIBILITY_DOMINANCE_ONLY" in doc
assert "RawToStructuredAdmissibilityDominance" in doc

print("STRUCTURED_ADMISSIBILITY_DOMINANCE_FOR_COMPUTABLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
