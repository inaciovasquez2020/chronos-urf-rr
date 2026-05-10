#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_SemanticObservationMapConstruction.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_SEMANTIC_OBSERVATION_MAP_CONSTRUCTION_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_semantic_observation_map_construction.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure H4_1_FGL_SemanticFinalCarrier",
    "Carrier : Type u",
    "Observation : Type v",
    "FinalHypothesis : Carrier → Prop",
    "FinalGapLeft : Carrier → Prop",
    "FinalGapRight : Carrier → Prop",
    "SoundnessPredicate : Carrier → Prop",
    "ObsSoundnessPredicate : Observation → Prop",
    "structure H4_1_FGL_SemanticObservationMap",
    "observe : S.Carrier → S.Observation",
    "structure H4_1_FGL_SemanticSeparatingObservable",
    "toObservation : S.Carrier → S.Observation",
    "def h4_1_fgl_construct_semantic_observation_map",
    "structure H4_1_FGL_SemanticObservationConstructionPackage",
    "def H4_1_FGL_SemanticObservationConstructionPackage.ofSeparatingObservable",
    "def H4_1_FGL_SemanticObservationConstructionPackage.toPropWitness",
    "theorem h4_1_fgl_semantic_observation_package_implies_missing_witness",
    "theorem h4_1_fgl_semantic_separating_observable_implies_missing_witness",
    "H4_1_FGL_MissingObservationExtractionWitness",
    "explicit separating observable",
    "does not prove that such an observable exists",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: CONDITIONAL_SEMANTIC_CONSTRUCTION",
    "`H4_1_FGL_SemanticFinalCarrier`",
    "`H4_1_FGL_SemanticObservationMap`",
    "`H4_1_FGL_SemanticSeparatingObservable`",
    "`h4_1_fgl_construct_semantic_observation_map`",
    "`h4_1_fgl_semantic_separating_observable_implies_missing_witness`",
    "Existence of an explicit separating observable",
    "does not prove unconditional separating observable existence",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "CONDITIONAL_SEMANTIC_CONSTRUCTION"
assert data["classification"] == "SEMANTIC_OBSERVATION_MAP_CONSTRUCTION"
assert data["semantic_extraction"] is True
assert data["condition"] == "explicit separating observable plus one selected final-carrier point"
assert "H4_1_FGL_SemanticObservationMap" in data["constructs"]
assert "H4_1_FGL_MissingObservationExtractionWitness" in data["closed_conditional_targets"]
assert "h4_1_fgl_construct_semantic_observation_map" in data["theorems"]
assert "h4_1_fgl_semantic_separating_observable_implies_missing_witness" in data["theorems"]
assert data["remaining_unconditional_frontier"] == "existence of an explicit separating observable for every selected final-carrier instance"
assert "unconditional separating observable existence" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_SemanticObservationMapConstruction" in rt

print("H4.1/FGL semantic observation-map construction verified: CONDITIONAL_SEMANTIC_CONSTRUCTION")
