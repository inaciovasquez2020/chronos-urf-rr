import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_concrete_analytic_package_bridge_artifact_status_and_target():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_bridge_2026_05_23.json").read_text())
    assert data["status"] == "BRIDGE_CANDIDATE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["target"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE"
    assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK"

def test_concrete_analytic_package_bridge_previous_ingredients_are_recorded():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_bridge_2026_05_23.json").read_text())
    assert "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE" in data["previous_ingredients"]
    assert "RESTRICTED_CONTINUATION_NORM_CONTROL" in data["previous_ingredients"]

def test_concrete_analytic_package_bridge_assumptions_are_explicit():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_bridge_2026_05_23.json").read_text())
    for token in [
        "restrictedConcentrationMonotonicity",
        "restrictedContinuationNormControl",
        "packageCompatibility",
        "targetInterfaceCompatibility",
    ]:
        assert token in data["assumptions"]

def test_concrete_analytic_package_bridge_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_bridge_2026_05_23.json").read_text())
    for token in [
        "no analytic Einstein-matter bootstrap package",
        "no concrete analytic Einstein-matter estimate package proof",
        "no finite continuation norm theorem",
        "no threshold crossing proof",
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]:
        assert token in data["boundary"]

def test_concrete_analytic_package_bridge_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageBridge.lean").read_text()
    for token in [
        "ConcreteAnalyticEinsteinMatterEstimatePackageBridgeData",
        "ConcreteAnalyticEinsteinMatterEstimatePackageBridgeHypotheses",
        "RestrictedLocalConcentrationData",
        "RestrictedLocalFluxTerms",
        "RestrictedContinuationNormData",
        "restrictedConcentrationMonotonicity",
        "restrictedContinuationNormControl",
        "ConcreteAnalyticEinsteinMatterEstimatePackageBridge",
    ]:
        assert token in text
