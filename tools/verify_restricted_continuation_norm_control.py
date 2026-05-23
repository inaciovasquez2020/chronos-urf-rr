#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/restricted_continuation_norm_control_2026_05_23.json"
doc = ROOT / "docs/status/RESTRICTED_CONTINUATION_NORM_CONTROL_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControl.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "RESTRICTED_CONTINUATION_NORM_CONTROL"
assert data["status"] == "CONTINUATION_NORM_CONTROL_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE"
assert data["previous_ingredient"] == "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE"
assert data["supplies_next_analytic_ingredient_for"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE"
assert data["conclusion"] == "continuation norm remains finite until Q reaches threshold"
assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE"

for token in [
    "continuationNormN",
    "bootstrapInequalitiesB",
    "concentrationFunctionalQ",
    "thresholdQ",
]:
    assert token in data["objects"]

for token in [
    "initialNormFinite",
    "bootstrapControlsNorm",
    "concentrationMonotone",
    "belowThresholdOnInterval",
    "localContinuationCriterion",
    "noBlowupBeforeThreshold",
]:
    assert token in data["assumptions"]

for boundary in [
    "candidate continuation-norm control only",
    "local continuation criterion assumed",
    "no-blowup-before-threshold estimate assumed",
    "no analytic Einstein-matter bootstrap package",
    "no concrete analytic Einstein-matter estimate package",
    "no threshold crossing proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
]:
    assert boundary in data["boundary"]

doc_text = doc.read_text()
assert "CONTINUATION_NORM_CONTROL_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE" in doc_text
assert "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE" in doc_text
assert "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE" in doc_text

lean_text = lean.read_text()
for token in [
    "RestrictedContinuationNormData",
    "RestrictedContinuationNormHypotheses",
    "continuationNormN",
    "bootstrapInequalitiesB",
    "concentrationFunctionalQ",
    "thresholdQ",
    "RestrictedContinuationNormControl",
    "localContinuationCriterion",
    "noBlowupBeforeThreshold",
]:
    assert token in lean_text

print("Restricted continuation norm control verifier OK.")
print("Status:", data["status"])
print("Supplies:", data["supplies_next_analytic_ingredient_for"])
