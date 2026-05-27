#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/Chronos/Frontier/FiniteSupportBridgeForComputableClass.lean"
ART = ROOT / "artifacts/chronos/finite_support_bridge_for_computable_class_2026_05_27.json"
DOC = ROOT / "docs/status/FINITE_SUPPORT_BRIDGE_FOR_COMPUTABLE_CLASS_2026_05_27.md"
ROOT_IMPORT = ROOT / "lean/Chronos.lean"

src = LEAN.read_text(errors="ignore")
data = json.loads(ART.read_text())
doc = DOC.read_text(errors="ignore")
root_import = ROOT_IMPORT.read_text(errors="ignore")

required_src = [
    "import Chronos.Frontier.ComputableFiniteAdmissibleClass",
    "structure FiniteSupportBridgeCertificate",
    "semantic_rank_le_entropy_gap",
    "theorem finite_support_bridge_from_certificate",
    "theorem finite_support_bridge_preserves_finite_support",
    "def FiniteSupportBridgeCertificateSupply",
    "theorem finite_support_bridge_from_supply",
]

for token in required_src:
    assert token in src, token

assert "import Chronos.Frontier.FiniteSupportBridgeForComputableClass" in root_import
assert data["status"] == "FINITE_SUPPORT_BRIDGE_CERTIFICATE_ONLY"
assert data["structural_action"] == 2
assert data["object"] == "FiniteSupportBridgeCertificate"

for boundary in [
    "certificate supply theorem",
    "finite-support bridge for every computable finite admissible class without certificate",
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

assert "FINITE_SUPPORT_BRIDGE_CERTIFICATE_ONLY" in doc
assert "FiniteSupportBridgeCertificate" in doc

print("FINITE_SUPPORT_BRIDGE_FOR_COMPUTABLE_CLASS_OK")
print(json.dumps({
    "status": data["status"],
    "object": data["object"],
    "next_missing_ingredient": data["next_missing_ingredient"],
}, indent=2, sort_keys=True))
