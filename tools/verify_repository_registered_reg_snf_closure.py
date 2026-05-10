#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

paths = {
    "lean": ROOT / "Chronos/Frontier/RepositoryRegisteredRegSNFClosure.lean",
    "frontier_lean": ROOT / "Chronos/Frontier/CarrierRegistryExhaustiveness.lean",
    "artifact": ROOT / "artifacts/chronos/repository_registered_reg_snf_closure.json",
    "frontier_artifact": ROOT / "artifacts/chronos/carrier_registry_exhaustiveness_frontier.json",
    "doc": ROOT / "docs/status/CHRONOS_REPOSITORY_REGISTERED_REG_SNF_CLOSURE_2026_05_10.md",
    "chronos": ROOT / "Chronos.lean",
}

for path in paths.values():
    assert path.exists(), path

lean_text = paths["lean"].read_text()
frontier_lean_text = paths["frontier_lean"].read_text()
artifact_text = paths["artifact"].read_text()
frontier_artifact_text = paths["frontier_artifact"].read_text()
doc_text = paths["doc"].read_text()
chronos_text = paths["chronos"].read_text()
data = json.loads(artifact_text)
frontier_data = json.loads(frontier_artifact_text)

required_tokens = [
    "WEAKENED_THEOREM_PACKAGE",
    "Reg-SNF closure for repository-registered carriers",
    "REPOSITORY_REGISTERED_CARRIERS_ONLY",
    "CarrierRegistryExhaustiveness remains FRONTIER_OPEN",
    "NO_UNRESTRICTED_REG_SNF_CLOSURE",
    "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF",
    "NO_UNIVERSAL_FIBER_ENTROPY_GAP_PROOF",
    "NO_DEPTH_BRIDGE_EXTENSION_BEYOND_SELECTED_FINAL_CARRIER_DOMAIN",
    "NO_CHRONOS_RR_CLOSURE",
    "NO_H4_1_FGL_CLOSURE",
    "NO_P_VS_NP_CLOSURE",
    "NO_CLAY_PROBLEM_CLOSURE",
]

for token in required_tokens:
    assert token in lean_text, token
    assert token in artifact_text, token

assert data["status"] == "WEAKENED_THEOREM_PACKAGE"
assert data["domain"] == "REPOSITORY_REGISTERED_CARRIERS_ONLY"
assert data["boundary"]["carrier_registry_exhaustiveness"] == "NO_CARRIER_REGISTRY_EXHAUSTIVENESS_PROOF"

assert frontier_data["status"] == "FRONTIER_OPEN"
assert "FRONTIER_OPEN" in frontier_lean_text

required_doc_phrases = [
    "Status: WEAKENED_THEOREM_PACKAGE",
    "REPOSITORY_REGISTERED_CARRIERS_ONLY",
    "CarrierRegistryExhaustiveness remains FRONTIER_OPEN.",
    "No unrestricted Reg-SNF closure.",
    "No CarrierRegistryExhaustiveness proof.",
    "No UniversalFiberEntropyGap proof.",
    "No DepthBridge extension beyond selected final carrier domain.",
    "No Chronos-RR closure.",
    "No H4.1/FGL closure.",
    "No P vs NP closure.",
    "No Clay-problem closure.",
]

for phrase in required_doc_phrases:
    assert phrase in doc_text, phrase

for import_line in [
    "import Chronos.Frontier.CarrierRegistryExhaustiveness",
    "import Chronos.Frontier.RepositoryRegisteredRegSNFClosure",
]:
    assert import_line in chronos_text, import_line

for forbidden in [
    "CarrierRegistryExhaustiveness is proved",
    "unrestricted Reg-SNF closure is proved",
    "UniversalFiberEntropyGap is proved",
    "DepthBridge is extended beyond selected final carrier domain",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is solved",
    "Clay problem is solved",
]:
    assert forbidden not in lean_text
    assert forbidden not in artifact_text
    assert forbidden not in doc_text

print("Repository-registered Reg-SNF closure package verified: WEAKENED_THEOREM_PACKAGE")
