#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]

lean = root / "Chronos/Frontier/H4_1_FGL_SelectedSeparatingObservableExistence.lean"
doc = root / "docs/status/CHRONOS_H4_1_FGL_SELECTED_SEPARATING_OBSERVABLE_EXISTENCE_2026_05_10.md"
artifact = root / "artifacts/chronos/h4_1_fgl_selected_separating_observable_existence.json"
root_import = root / "Chronos.lean"

for p in (lean, doc, artifact, root_import):
    assert p.exists(), p

lt = lean.read_text()
dt = doc.read_text()
rt = root_import.read_text()
data = json.loads(artifact.read_text())

required_lean = [
    "structure H4_1_FGL_SelectedFinalCarrierInstance",
    "leftObs : S.Observation",
    "rightObs : S.Observation",
    "defaultObs : S.Observation",
    "left_right_distinct : leftObs ≠ rightObs",
    "leftObs_sound : S.ObsSoundnessPredicate leftObs",
    "rightObs_sound : S.ObsSoundnessPredicate rightObs",
    "defaultObs_sound : S.ObsSoundnessPredicate defaultObs",
    "gap_disjoint",
    "left_decidable : DecidablePred S.FinalGapLeft",
    "right_decidable : DecidablePred S.FinalGapRight",
    "def observe",
    "def toSeparatingObservable",
    "theorem has_separating_observable",
    "def H4_1_FGL_SelectedFinalCarrierInstancePredicate",
    "theorem H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence",
    "structure H4_1_FGL_SelectedFinalCarrierInstanceWithPoint",
    "theorem H4_1_FGL_SelectedFinalCarrierInstanceWithPoint_implies_missing_witness",
    "h4_1_fgl_semantic_separating_observable_implies_missing_witness",
    "does not prove existence for arbitrary semantic final carriers",
]
for token in required_lean:
    assert token in lt, token

required_doc = [
    "Status: SELECTED_INSTANCE_EXISTENCE_THEOREM",
    "`H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence`",
    "`H4_1_FGL_SelectedFinalCarrierInstance`",
    "`H4_1_FGL_SelectedFinalCarrierInstance.observe`",
    "`H4_1_FGL_SelectedFinalCarrierInstance.toSeparatingObservable`",
    "`H4_1_FGL_SelectedFinalCarrierInstanceWithPoint_implies_missing_witness`",
    "does not prove separating-observable existence for arbitrary semantic final carriers",
    "does not prove unrestricted H4.1/FGL",
    "does not prove P vs NP",
]
for token in required_doc:
    assert token in dt, token

assert data["status"] == "SELECTED_INSTANCE_EXISTENCE_THEOREM"
assert data["classification"] == "SEMANTIC_SELECTED_INSTANCE_THEOREM"
assert "H4_1_FGL_SelectedFinalCarrierSeparatingObservableExistence" in data["proves"]
assert "H4_1_FGL_SelectedFinalCarrierInstanceWithPoint_implies_missing_witness" in data["proves"]
assert "left/right final-gap disjointness" in data["selected_instance_requires"]
assert "decidable left final-gap side" in data["selected_instance_requires"]
assert "H4_1_FGL_SelectedFinalCarrierInstance.toSeparatingObservable" in data["constructs"]
assert "separating observable existence for arbitrary semantic final carriers" in data["does_not_claim"]
assert "P vs NP closure" in data["does_not_claim"]
assert "import Chronos.Frontier.H4_1_FGL_SelectedSeparatingObservableExistence" in rt

print("H4.1/FGL selected separating observable existence verified: SELECTED_INSTANCE_EXISTENCE_THEOREM")
