#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/CertificateSupplyLawForComputableClass.lean"
ART = ROOT / "artifacts/chronos/certificate_supply_law_for_computable_class_2026_05_27.json"
DOC = ROOT / "docs/status/CERTIFICATE_SUPPLY_LAW_FOR_COMPUTABLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "import Chronos.Frontier.FiniteSupportBridgeForComputableClass",
    "def FiniteSupportBridgeLawForComputableClass : Prop",
    "theorem certificate_supply_from_finite_support_bridge_law",
    "theorem finite_support_bridge_from_law",
    "def IntrinsicFiniteSupportBridgeLawProblem : Prop",
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.CertificateSupplyLawForComputableClass" in root_import
assert data["status"] == "CERTIFICATE_SUPPLY_FROM_EXPLICIT_LAW_ONLY"
assert data["structural_action"] == 3
assert data["object"] == "FiniteSupportBridgeLawForComputableClass"

for boundary in [
    "intrinsic finite-support bridge law",
    "certificate supply theorem without explicit law",
    "bridge for every computable finite admissible class from raw admissibility alone",
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

assert "CERTIFICATE_SUPPLY_FROM_EXPLICIT_LAW_ONLY" in doc
assert "IntrinsicFiniteSupportBridgeLawProblem" in doc

print("CERTIFICATE_SUPPLY_LAW_FOR_COMPUTABLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
