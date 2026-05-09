#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json"
doc = ROOT / "docs/status/CHRONOS_CARRIER_REGISTRY_EXHAUSTIVENESS_FRONTIER_2026_05_09.md"
data = json.loads(artifact.read_text())
text = doc.read_text()
assert data["status"] == "FRONTIER_OPEN"
assert data["minimal_missing_lemma"] == "CarrierRegistryExhaustiveness"
assert "zero-arity admissible predicate counterexample" in data["blocked_by"]
assert "Frontier statement only" in data["boundary"]
required = [
"Status: FRONTIER_OPEN",
"CarrierRegistryExhaustiveness:",
"zero-arity admissible predicate counterexample",
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
print("CarrierRegistryExhaustiveness frontier verified: FRONTIER_OPEN")
