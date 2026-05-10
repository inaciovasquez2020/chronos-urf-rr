#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_FinalCarrierObservationExtraction.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_FINAL_CARRIER_OBSERVATION_EXTRACTION_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_final_carrier_observation_extraction.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "H4_1_FGL_FinalCarrierObservationExtractionFrontier",
    "H4_1_FGL_FinalCarrierObservationExtraction",
    "frontier_open := True",
    "selected_final_carrier_domain_only := True",
    "no_unrestricted_h4_1_fgl_closure := True",
    "no_chronos_rr_closure := True",
    "no_p_vs_np_closure := True",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: FRONTIER_OPEN",
    "`H4_1_FGL_FinalCarrierObservationExtraction`",
    "Selected final-carrier domain only.",
    "does not prove final selected-carrier soundness",
    "does not prove unrestricted H4.1/FGL closure",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "FRONTIER_OPEN"
assert data["classification"] == "MISSING_THEOREM_LEVEL_OBSERVATION_EXTRACTION"
assert data["domain"] == "SELECTED_FINAL_CARRIER_DOMAIN_ONLY"
assert data["weakest_missing_object"] == "H4_1_FGL_FinalCarrierObservationExtraction"
assert "H4_1_FGL_FinalCarrierSelectedGapSoundness" in data["feeds"]
assert "unrestricted H4.1/FGL closure" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_FinalCarrierObservationExtraction" in rt

print("H4.1/FGL final carrier observation extraction frontier verified: FRONTIER_OPEN")
