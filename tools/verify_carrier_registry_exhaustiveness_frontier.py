#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

lean = ROOT / "Chronos/Frontier/CarrierRegistryExhaustiveness.lean"
artifact = ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json"
doc = ROOT / "docs/status/CHRONOS_CARRIER_REGISTRY_EXHAUSTIVENESS_FRONTIER_2026_05_10.md"
chronos = ROOT / "Chronos.lean"

for path in (lean, artifact, doc, chronos):
    assert path.exists(), path

lean_text = lean.read_text()
doc_text = doc.read_text()
chronos_text = chronos.read_text()
data = json.loads(artifact.read_text())

required_tokens = [
    "FRONTIER_OPEN",
    "CarrierRegistryExhaustiveness",
    "NO_CHRONOS_RR_CLOSURE",
    "NO_H4_1_FGL_CLOSURE",
    "NO_P_VS_NP_CLOSURE",
    "NO_CLAY_PROBLEM_CLOSURE",
    "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF",
    "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN",
]

for token in required_tokens:
    assert token in lean_text, token
    assert token in artifact.read_text(), token

required_doc_phrases = [
    "Status: FRONTIER_OPEN",
    "No Chronos-RR closure.",
    "No H4.1/FGL closure.",
    "No P vs NP closure.",
    "No Clay-problem closure.",
    "No UniversalFiberEntropyGap proof.",
    "No DepthBridge extension beyond selected final carrier domain.",
    "No unrestricted Reg-SNF closure is claimed by this artifact.",
]

for phrase in required_doc_phrases:
    assert phrase in doc_text, phrase

assert data["status"] == "FRONTIER_OPEN"
assert data["weakest_missing_lemma"] == "CarrierRegistryExhaustiveness"
assert "import Chronos.Frontier.CarrierRegistryExhaustiveness" in chronos_text

for forbidden in [
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is solved",
    "Clay problem is solved",
    "UniversalFiberEntropyGap is proved",
    "DepthBridge is extended beyond selected final carrier domain",
    "unrestricted Reg-SNF closure is proved"
]:
    assert forbidden not in doc_text
    assert forbidden not in lean_text
    assert forbidden not in artifact.read_text()

print("CarrierRegistryExhaustiveness frontier verified: FRONTIER_OPEN")
