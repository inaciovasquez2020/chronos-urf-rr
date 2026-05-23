import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_continuation_norm_control_artifact_status_and_target():
    data = json.loads((ROOT / "artifacts/chronos/restricted_continuation_norm_control_2026_05_23.json").read_text())
    assert data["status"] == "CONTINUATION_NORM_CONTROL_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE"
    assert data["previous_ingredient"] == "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE"
    assert data["supplies_next_analytic_ingredient_for"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE"
    assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE"

def test_restricted_continuation_norm_control_assumptions_are_explicit():
    data = json.loads((ROOT / "artifacts/chronos/restricted_continuation_norm_control_2026_05_23.json").read_text())
    for token in [
        "initialNormFinite",
        "bootstrapControlsNorm",
        "concentrationMonotone",
        "belowThresholdOnInterval",
        "localContinuationCriterion",
        "noBlowupBeforeThreshold",
    ]:
        assert token in data["assumptions"]

def test_restricted_continuation_norm_control_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/restricted_continuation_norm_control_2026_05_23.json").read_text())
    for token in [
        "no analytic Einstein-matter bootstrap package",
        "no concrete analytic Einstein-matter estimate package",
        "no threshold crossing proof",
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]:
        assert token in data["boundary"]

def test_restricted_continuation_norm_control_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedContinuationNormControl.lean").read_text()
    for token in [
        "RestrictedContinuationNormData",
        "RestrictedContinuationNormHypotheses",
        "continuationNormN",
        "bootstrapInequalitiesB",
        "concentrationFunctionalQ",
        "thresholdQ",
        "RestrictedContinuationNormControl",
        "noBlowupBeforeThreshold",
    ]:
        assert token in text
