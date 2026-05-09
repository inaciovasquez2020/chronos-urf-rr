#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/zero_arity_bifurcation_lock.json"
DOC = ROOT / "docs/status/CHRONOS_ZERO_ARITY_BIFURCATION_LOCK_2026_05_09.md"

data = json.loads(ARTIFACT.read_text())
text = DOC.read_text()

assert data["id"] == "CHRONOS_ZERO_ARITY_BIFURCATION_LOCK_2026_05_09"
assert data["status"] == "BIFURCATION_LOCKED"
assert data["decision_lock_dependency"] == "CHRONOS_ADMISSIBILITY_POSITIVITY_DECISION_LOCK_2026_05_09"
assert data["weakest_sufficient_completion"] == "ZeroArityExclusion OR ZeroArityRepresentation"
assert data["accepted_paths"] == ["ZeroArityExclusion", "ZeroArityRepresentation"]

required_doc_tokens = [
    "Status: BIFURCATION_LOCKED",
    "ZeroArityExclusion",
    "ZeroArityRepresentation",
    "Weakest sufficient completion:",
    "ZeroArityExclusion OR ZeroArityRepresentation",
    "does not prove ZeroArityExclusion",
    "does not prove ZeroArityRepresentation",
    "does not resolve ZeroArityCarrierObstruction",
    "does not prove CarrierRegistryExhaustiveness",
    "does not prove Reg-SNF",
    "does not prove UniversalFiberEntropyGap",
    "does not prove DepthBridge",
    "does not close Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem",
]

for token in required_doc_tokens:
    assert token in text, token

for claim in data["forbidden_claims"]:
    assert claim not in text, claim

print("ZeroArityBifurcationLock verified: BIFURCATION_LOCKED")
