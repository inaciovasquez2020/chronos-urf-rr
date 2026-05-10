#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_FinalSelectedInputClosure.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_FINAL_SELECTED_INPUT_CLOSURE_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_final_selected_input_closure.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure H4_1_FGL_FinalSelectedInput",
    "domain : H4_1_FGL_SelectedTheoremDomain",
    "def H4_1_FGL_FinalSelectedInput.toSelectedTheoremDomain",
    "theorem H4_1_FGL_FinalSelectedInput_has_separating_observable",
    "theorem H4_1_FGL_FinalSelectedInput_implies_missing_observation_extraction_witness",
    "theorem H4_1_FGL_FinalSelectedInput_implies_final_carrier_observation_extraction_target",
    "structure H4_1_FGL_FinalSelectedInputClosure",
    "def H4_1_FGL_FinalSelectedInputClosure.ofInput",
    "theorem H4_1_FGL_FinalSelectedInput_closes_selected_observation_layer",
    "none inside selected-domain observation-extraction layer",
    "does not claim arbitrary semantic final-carrier",
    "does not claim arbitrary semantic final-carrier closure",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: SELECTED_DOMAIN_OBSERVATION_LAYER_CLOSED",
    "`H4_1_FGL_FinalSelectedInput`",
    "`H4_1_FGL_SelectedTheoremDomain`",
    "explicit separating observable existence",
    "`H4_1_FGL_MissingObservationExtractionWitness`",
    "`H4_1_FGL_FinalCarrierObservationExtractionTarget`",
    "`H4_1_FGL_FinalSelectedInputClosure`",
    "`H4_1_FGL_FinalSelectedInput_closes_selected_observation_layer`",
    "does not claim arbitrary semantic final-carrier closure",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "SELECTED_DOMAIN_OBSERVATION_LAYER_CLOSED"
assert data["classification"] == "FINAL_SELECTED_INPUT_CLOSURE"
assert data["new_input"] == "H4_1_FGL_FinalSelectedInput"
assert data["theorem_domain"] == "H4_1_FGL_SelectedTheoremDomain"
assert "explicit separating observable existence" in data["closes_on_selected_domain"]
assert "H4_1_FGL_MissingObservationExtractionWitness" in data["closes_on_selected_domain"]
assert "H4_1_FGL_FinalCarrierObservationExtractionTarget" in data["closes_on_selected_domain"]
assert "H4_1_FGL_FinalSelectedInput_closes_selected_observation_layer" in data["proves"]
assert data["remaining_frontier"] == "none inside selected-domain observation-extraction layer"
assert "arbitrary semantic final-carrier closure" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_FinalSelectedInputClosure" in rt

print("H4.1/FGL final selected input closure verified: SELECTED_DOMAIN_OBSERVATION_LAYER_CLOSED")
