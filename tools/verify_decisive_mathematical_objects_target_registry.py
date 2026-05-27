#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/chronos/decisive_mathematical_objects_target_registry_2026_05_27.json")
DOC = Path("docs/status/DECISIVE_MATHEMATICAL_OBJECTS_TARGET_REGISTRY_2026_05_27.md")
LEAN = Path("lean/Chronos/Frontier/DecisiveMathematicalObjectsTargetRegistry.lean")

assert ART.exists(), f"missing artifact: {ART}"
assert DOC.exists(), f"missing doc: {DOC}"
assert LEAN.exists(), f"missing Lean file: {LEAN}"

data = json.loads(ART.read_text())

required_targets = {
    "RankEntropyGapLemma",
    "FiniteToUniformUpgradeLemma",
    "LowerBoundInequality",
    "CompactnessTheorem",
    "RealNumericalPredictionVectorRun",
}

required_boundaries = required_targets | {
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted gravity closure",
}

doc = DOC.read_text()
lean = LEAN.read_text()
target_names = {target["name"] for target in data["targets"]}
target_statuses = {target["status"] for target in data["targets"]}
weakest_objects = [target["weakest_sufficient_object"] for target in data["targets"]]

assert data["id"] == "DECISIVE_MATHEMATICAL_OBJECTS_TARGET_REGISTRY_2026_05_27"
assert data["status"] == "OPEN_TARGET_REGISTRY_ONLY_NO_MATHEMATICAL_CLOSURE"
assert data["central_mathematical_slogan"] == "Nontrivial registered structure forces a nonzero quantitative gap."
assert len(data["targets"]) == 5
assert target_names == required_targets
assert target_statuses <= {"OPEN_TARGET_NOT_PROVED", "OPEN_TARGET_NOT_EXECUTED"}
assert all(weakest_objects)
assert data["current_state"]["infrastructure"] == "substantially improved"
assert data["current_state"]["mathematical_closure"] == "not finished"
assert data["current_state"]["prediction_vector_closure"] == "not finished"
assert required_boundaries.issubset(set(data["does_not_prove"]))
assert required_targets <= set(doc.split()) or all(name in doc for name in required_targets)
assert all(name in lean for name in required_targets)
assert "OPEN_TARGET_REGISTRY_ONLY_NO_MATHEMATICAL_CLOSURE" in doc
assert "Nontrivial registered structure forces a nonzero quantitative gap." in doc
assert "decisiveMathematicalObjectTargets_length" in lean
assert "centralMathematicalSlogan" in lean

print("DECISIVE_MATHEMATICAL_OBJECTS_TARGET_REGISTRY_OK")
