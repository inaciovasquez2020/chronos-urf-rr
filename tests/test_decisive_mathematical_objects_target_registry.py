import json
from pathlib import Path
ART = Path("artifacts/chronos/decisive_mathematical_objects_target_registry_2026_05_27.json")
DOC = Path("docs/status/DECISIVE_MATHEMATICAL_OBJECTS_TARGET_REGISTRY_2026_05_27.md")
LEAN = Path("lean/Chronos/Frontier/DecisiveMathematicalObjectsTargetRegistry.lean")
def data(): return json.loads(ART.read_text())
def test_registry_status_is_open_target_only(): assert data()["status"] == "OPEN_TARGET_REGISTRY_ONLY_NO_MATHEMATICAL_CLOSURE"
def test_registry_has_five_decisive_targets(): assert len(data()["targets"]) == 5
def test_current_state_remains_not_finished(): state = data()["current_state"]; assert state["mathematical_closure"] == "not finished"; assert state["prediction_vector_closure"] == "not finished"
def test_boundaries_block_major_promotions(): blocked = set(data()["does_not_prove"]); assert "unrestricted Chronos-RR" in blocked; assert "P vs NP" in blocked; assert "any Clay problem" in blocked; assert "DFM-MKC empirical validation" in blocked
def test_doc_and_lean_bind_targets(): text = DOC.read_text() + "\n" + LEAN.read_text(); assert "RankEntropyGapLemma" in text; assert "FiniteToUniformUpgradeLemma" in text; assert "LowerBoundInequality" in text; assert "CompactnessTheorem" in text; assert "RealNumericalPredictionVectorRun" in text
