#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_FormalObservationExtractionWitness.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_FORMAL_OBSERVATION_EXTRACTION_WITNESS_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_formal_observation_extraction_witness.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "import Chronos.Frontier.H4_1_FGL_ObservationExtractionWitnessInterface",
    "def H4_1_FGL_FormalObservationExtractionWitness",
    "selected_final_carrier_domain := True",
    "observation_map_exists := True",
    "observation_separates_final_carrier_gap := True",
    "observation_preserves_selected_carrier_soundness := True",
    "theorem h4_1_fgl_missing_observation_extraction_witness_solved",
    "H4_1_FGL_MissingObservationExtractionWitness",
    "theorem h4_1_fgl_final_carrier_observation_extraction_target_solved",
    "H4_1_FGL_FinalCarrierObservationExtractionTarget",
    "h4_1_fgl_missing_witness_equiv_target.mp",
    "theorem h4_1_fgl_formal_witness_completion_boundary",
    "not a semantic extraction theorem",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: FORMAL_PROP_COMPLETION_ONLY",
    "`H4_1_FGL_MissingObservationExtractionWitness`",
    "`h4_1_fgl_missing_observation_extraction_witness_solved`",
    "`h4_1_fgl_final_carrier_observation_extraction_target_solved`",
    "`h4_1_fgl_formal_witness_completion_boundary`",
    "does not construct a semantic observation map",
    "does not prove a semantic extraction theorem",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "FORMAL_PROP_COMPLETION_ONLY"
assert data["classification"] == "PROPOSITION_VALUED_INTERFACE_COMPLETION"
assert data["semantic_extraction"] is False
assert "H4_1_FGL_MissingObservationExtractionWitness" in data["closed_formal_targets"]
assert "H4_1_FGL_FinalCarrierObservationExtractionTarget" in data["closed_formal_targets"]
assert "h4_1_fgl_missing_observation_extraction_witness_solved" in data["closed_theorems"]
assert "h4_1_fgl_final_carrier_observation_extraction_target_solved" in data["closed_theorems"]
assert "h4_1_fgl_formal_witness_completion_boundary" in data["closed_theorems"]
assert data["remaining_semantic_frontier"] == "semantic observation-map construction"
assert "semantic observation map construction" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_FormalObservationExtractionWitness" in rt

print("H4.1/FGL formal observation extraction witness verified: FORMAL_PROP_COMPLETION_ONLY")
