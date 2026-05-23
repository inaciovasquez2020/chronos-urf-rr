#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_proof_obligation_lock_2026_05_23.json"
doc = ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLock.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK"
assert data["status"] == "PROOF_OBLIGATION_LOCK_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
assert data["previous_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE"
assert data["next_admissible_object"] == "LOCAL_BALANCE_LAW_DQDT_DERIVATION"

remaining = [
    "LOCAL_BALANCE_LAW_DQDT_DERIVATION",
    "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF",
    "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
    "PACKAGE_COMPATIBILITY_PROOF",
    "TARGET_INTERFACE_COMPATIBILITY_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
]
for token in remaining:
    assert token in data["remaining_next_admissible_objects"]

for boundary in [
    "proof-obligation lock only",
    "no local balance law dQ/dt derivation",
    "no restricted concentration monotonicity proof",
    "no restricted continuation norm control proof",
    "no package compatibility proof",
    "no target-interface compatibility proof",
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
    "PROOF_OBLIGATION_LOCK_ONLY_NO_ANALYTIC_PACKAGE_PROOF",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE",
    "LOCAL_BALANCE_LAW_DQDT_DERIVATION",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
]:
    assert token in doc_text

lean_text = lean.read_text()
for token in [
    "ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLockData",
    "ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLockHypotheses",
    "localBalanceLawDQDTDerivation",
    "restrictedConcentrationMonotonicityProof",
    "restrictedContinuationNormControlProof",
    "packageCompatibilityProof",
    "targetInterfaceCompatibilityProof",
    "concreteAnalyticEstimatePackageProof",
    "ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLock",
]:
    assert token in lean_text

print("Concrete analytic Einstein-matter estimate package proof-obligation lock verifier OK.")
print("Status:", data["status"])
print("Next admissible object:", data["next_admissible_object"])
