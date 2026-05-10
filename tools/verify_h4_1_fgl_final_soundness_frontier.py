#!/usr/bin/env python3
from pathlib import Path
import json

lean = Path("Chronos/Frontier/H4_1_FGL_FinalSoundnessFrontier.lean").read_text()
doc = Path("docs/status/CHRONOS_H4_1_FGL_FINAL_SOUNDNESS_FRONTIER_2026_05_10.md").read_text()
artifact = json.loads(Path("artifacts/chronos/h4_1_fgl_final_soundness_frontier.json").read_text())

required_lean = [
    "H4_1_FGL_FinalCarrierSelectedGapSoundnessFrontier",
    "H4_1_FGL_SelectedDepthBridgeSemanticSeparation",
    "h4_1_fgl_selected_depth_bridge_semantic_separation",
    "H4_1_FGL_FinalCarrierObservationExtraction",
    "h4_1_fgl_observation_extraction_to_semantic_gap",
    "FRONTIER_OPEN / FINAL_CARRIER_SELECTED_GAP_SOUNDNESS_REQUIRES_OBSERVATION_EXTRACTION",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "FRONTIER_OPEN"
assert artifact["frontier"] == "H4_1_FGL_FinalCarrierSelectedGapSoundness"
assert artifact["weakest_missing_ingredient"] == "H4_1_FGL_FinalCarrierObservationExtraction"

required_doc = [
    "Status: **FRONTIER_OPEN**",
    "No unrestricted H4.1/FGL closure",
    "No FinalCarrierSelectedGapSoundness proof",
    "No UniversalFiberEntropyGap theorem",
    "No Chronos-RR closure",
    "No P vs NP or Clay-problem closure",
]

for token in required_doc:
    assert token in doc, token

print("H4.1/FGL final soundness frontier verified: FRONTIER_OPEN")
