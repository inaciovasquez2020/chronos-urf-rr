#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

paths = {
    "lean": ROOT / "Chronos/Frontier/CarrierSupportSignatureInvariant.lean",
    "artifact": ROOT / "artifacts/chronos/carrier_support_signature_invariant.json",
    "doc": ROOT / "docs/status/CHRONOS_CARRIER_SUPPORT_SIGNATURE_INVARIANT_2026_05_10.md",
    "chronos": ROOT / "Chronos.lean",
}

for path in paths.values():
    assert path.exists(), path

lean_text = paths["lean"].read_text()
artifact_text = paths["artifact"].read_text()
doc_text = paths["doc"].read_text()
chronos_text = paths["chronos"].read_text()
data = json.loads(artifact_text)

required_tokens = [
    "CONDITIONAL_CLASSIFICATION_INVARIANT",
    "CarrierSupportSignatureInvariant",
    "conditional_carrier_registry_exhaustiveness_from_support_signature",
    "finite support signature classification",
    "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF",
    "NO_UNRESTRICTED_REG_SNF_CLOSURE",
    "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF",
    "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN",
    "NO_CHRONOS_RR_CLOSURE",
    "NO_H4_1_FGL_CLOSURE",
    "NO_P_VS_NP_CLOSURE",
    "NO_CLAY_PROBLEM_CLOSURE"
]

for token in required_tokens:
    assert token in lean_text or token in artifact_text or token in doc_text, token

assert data["status"] == "CONDITIONAL_CLASSIFICATION_INVARIANT"
assert data["new_ingredient"] == "finite support signature classification"
assert data["boundary"]["carrier_registry_exhaustiveness"] == "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF"
assert "import Chronos.Frontier.CarrierSupportSignatureInvariant" in chronos_text

required_doc_phrases = [
    "Status: CONDITIONAL_CLASSIFICATION_INVARIANT",
    "CarrierRegistryExhaustiveness remains FRONTIER_OPEN",
    "No CarrierRegistryExhaustiveness proof.",
    "No unrestricted Reg-SNF closure.",
    "No UniversalFiberEntropyGap proof.",
    "No DepthBridge extension beyond selected final carrier domain.",
    "No Chronos-RR closure.",
    "No H4.1/FGL closure.",
    "No P vs NP closure.",
    "No Clay-problem closure."
]

for phrase in required_doc_phrases:
    assert phrase in doc_text, phrase

for forbidden in [
    "CarrierRegistryExhaustiveness is proved",
    "unrestricted Reg-SNF closure is proved",
    "UniversalFiberEntropyGap is proved",
    "DepthBridge is extended beyond selected final carrier domain",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is solved",
    "Clay problem is solved"
]:
    assert forbidden not in lean_text
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("CarrierSupportSignatureInvariant verified: CONDITIONAL_CLASSIFICATION_INVARIANT")
