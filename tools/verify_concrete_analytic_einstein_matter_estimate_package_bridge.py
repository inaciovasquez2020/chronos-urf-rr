#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_bridge_2026_05_23.json"
doc = ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageBridge.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE"
assert data["status"] == "BRIDGE_CANDIDATE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
assert data["target"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE"
assert data["next_admissible_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK"

for token in [
    "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL",
]:
    assert token in data["previous_ingredients"]

for token in [
    "restrictedConcentrationMonotonicity",
    "restrictedContinuationNormControl",
    "packageCompatibility",
    "targetInterfaceCompatibility",
]:
    assert token in data["assumptions"]

for boundary in [
    "bridge candidate only",
    "restricted concentration monotonicity assumed",
    "restricted continuation norm control assumed",
    "package compatibility assumed",
    "target-interface compatibility assumed",
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
    assert boundary in data["boundary"]

doc_text = doc.read_text()
for token in [
    "BRIDGE_CANDIDATE_ONLY_NO_ANALYTIC_PACKAGE_PROOF",
    "RESTRICTED_LOCAL_CONCENTRATION_MONOTONICITY_WITH_FLUX_DOMINANCE",
    "RESTRICTED_CONTINUATION_NORM_CONTROL",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK",
]:
    assert token in doc_text

lean_text = lean.read_text()
for token in [
    "ConcreteAnalyticEinsteinMatterEstimatePackageBridgeData",
    "ConcreteAnalyticEinsteinMatterEstimatePackageBridgeHypotheses",
    "RestrictedLocalConcentrationData",
    "RestrictedLocalFluxTerms",
    "RestrictedContinuationNormData",
    "restrictedConcentrationMonotonicity",
    "restrictedContinuationNormControl",
    "packageCompatibility",
    "targetInterfaceCompatibility",
    "ConcreteAnalyticEinsteinMatterEstimatePackageBridge",
]:
    assert token in lean_text

print("Concrete analytic Einstein-matter estimate package bridge verifier OK.")
print("Status:", data["status"])
print("Target:", data["target"])
