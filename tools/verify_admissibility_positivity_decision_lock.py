#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/admissibility_positivity_decision_lock.json"
doc = ROOT / "docs/status/CHRONOS_ADMISSIBILITY_POSITIVITY_DECISION_LOCK_2026_05_09.md"
data = json.loads(artifact.read_text())
text = doc.read_text()
assert data["status"] == "DECISION_LOCKED"
assert data["blocked_theorem"] == "ZeroArityExclusion"
assert "permit zero-arity" in data["decision"]
assert "PositiveArityAdmissibility" in data["minimal_missing_assumption_for_exclusion"]
assert data["viable_route_without_semantic_change"] == "ZeroArityRepresentation"
assert "Decision lock only" in data["boundary"]
required = [
"Status: DECISION_LOCKED",
"Current RealChronosAdmissiblePredicate semantics permit zero-arity.",
"ZeroArityExclusion:",
"PositiveArityAdmissibility:",
"ZeroArityRepresentation:",
"Strengthen RealChronosAdmissiblePredicate with positive arity.",
"This file does not prove ZeroArityExclusion.",
"This file does not prove ZeroArityRepresentation.",
"This file does not resolve ZeroArityCarrierObstruction.",
"This file does not prove CarrierRegistryExhaustiveness.",
"This file does not prove Reg-SNF.",
"This file does not prove UniversalFiberEntropyGap.",
"This file does not prove DepthBridge.",
"This file does not prove Chronos-RR.",
"This file does not prove H4.1/FGL.",
"This file does not prove P vs NP.",
"This file does not prove any Clay problem."
]
for token in required:
    assert token in text, token
forbidden_promotions = [
"This file proves ZeroArityExclusion",
"This file proves ZeroArityRepresentation",
"This file resolves ZeroArityCarrierObstruction",
"This file proves CarrierRegistryExhaustiveness",
"This file proves Reg-SNF",
"This file proves UniversalFiberEntropyGap",
"This file proves DepthBridge",
"This file proves Chronos-RR",
"This file proves H4.1/FGL",
"This file proves P vs NP",
"This file proves any Clay problem"
]
for phrase in forbidden_promotions:
    assert phrase not in text, phrase
print("AdmissibilityPositivityDecisionLock verified: DECISION_LOCKED")
