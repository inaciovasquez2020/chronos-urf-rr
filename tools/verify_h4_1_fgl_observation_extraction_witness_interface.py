#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_ObservationExtractionWitnessInterface.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_OBSERVATION_EXTRACTION_WITNESS_INTERFACE_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_observation_extraction_witness_interface.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure H4_1_FGL_ObservationExtractionWitness",
    "selected_final_carrier_domain : Prop",
    "observation_map_exists : Prop",
    "observation_separates_final_carrier_gap : Prop",
    "observation_preserves_selected_carrier_soundness : Prop",
    "H4_1_FGL_FinalCarrierObservationExtractionTarget",
    "h4_1_fgl_observation_extraction_witness_implies_target",
    "H4_1_FGL_MissingObservationExtractionWitness",
    "h4_1_fgl_missing_witness_equiv_target",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: WITNESS_INTERFACE_ONLY",
    "`H4_1_FGL_FinalCarrierObservationExtraction`",
    "`H4_1_FGL_MissingObservationExtractionWitness`",
    "observation_map_exists",
    "observation_separates_final_carrier_gap",
    "observation_preserves_selected_carrier_soundness",
    "does not construct the observation-extraction witness",
    "does not prove unrestricted H4.1/FGL closure",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "WITNESS_INTERFACE_ONLY"
assert data["classification"] == "REDUCTION_INTERFACE"
assert data["input_frontier"] == "H4_1_FGL_FinalCarrierObservationExtraction"
assert data["new_weakest_missing_object"] == "H4_1_FGL_MissingObservationExtractionWitness"
assert "observation_map_exists" in data["required_witness_fields"]
assert "observation_separates_final_carrier_gap" in data["required_witness_fields"]
assert "observation_preserves_selected_carrier_soundness" in data["required_witness_fields"]
assert "construction of the observation-extraction witness" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_ObservationExtractionWitnessInterface" in rt

print("H4.1/FGL observation extraction witness interface verified: WITNESS_INTERFACE_ONLY")
