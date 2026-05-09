#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/zero_arity_representation_interface.json"
doc = ROOT / "docs/status/CHRONOS_ZERO_ARITY_REPRESENTATION_INTERFACE_2026_05_09.md"

data = json.loads(artifact.read_text())
text = doc.read_text()

assert data["status"] == "FRONTIER_OPEN"
assert data["interface"] == "ZeroArityRepresentationInterface"
assert "exists C in RegisteredChronosCarriers" in data["minimal_theorem_target"]
assert "no ZeroArityRepresentation proof or downstream theorem-level closure asserted" in data["boundary"]

required = [
    "Status: FRONTIER_OPEN",
    "ZeroArityRepresentation:",
    "∀ P, ZeroArityPredicate P ∧ RealChronosAdmissiblePredicate P →",
    "∃ C ∈ RegisteredChronosCarriers, Represents C P",
    "ZeroArityExclusion:",
    "This file does not prove ZeroArityRepresentation.",
    "This file does not prove ZeroArityExclusion.",
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

print("ZeroArityRepresentation interface verified: FRONTIER_OPEN")
