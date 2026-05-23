#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json"
doc = ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageCloseoutStack.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK"
assert data["status"] == "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
assert data["previous_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"
assert data["next_build_status"] == "NEXT_BUILD_ALLOWED_AFTER_STOP_LOCK"

expected_objects = [
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "PACKAGE_COMPATIBILITY_PROOF",
    "TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BUILD_STOP_LOCK",
]
assert data["remaining_next_admissible_objects_closed_as_surfaces"] == expected_objects

for boundary in [
    "closeout stack only",
    "proof surfaces only",
    "restricted continuation norm control proof surface only",
    "package compatibility proof surface only",
    "target-interface compatibility proof surface only",
    "concrete analytic Einstein-matter estimate package proof surface only",
    "no analytic derivation of the local balance law",
    "no unconditional restricted concentration monotonicity theorem",
    "no unconditional restricted continuation norm theorem",
    "no analytic Einstein-matter bootstrap package",
    "no concrete analytic Einstein-matter estimate package proof",
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
    "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "PACKAGE_COMPATIBILITY_PROOF",
    "TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
    "NEXT_BUILD_ALLOWED_AFTER_STOP_LOCK",
]:
    assert token in doc_text

lean_text = lean.read_text()
for token in [
    "RestrictedContinuationNormControlProof",
    "PackageCompatibilityProof",
    "TargetInterfaceCompatibilityProof",
    "ConcreteAnalyticEinsteinMatterEstimatePackageProof",
    "ConcreteAnalyticEinsteinMatterEstimatePackageBuildStopLock",
    "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF",
    "NEXT_BUILD_ALLOWED_AFTER_STOP_LOCK",
]:
    assert token in lean_text

print("Concrete analytic Einstein-matter estimate package closeout stack verifier OK.")
print("Status:", data["status"])
print("Next build status:", data["next_build_status"])
