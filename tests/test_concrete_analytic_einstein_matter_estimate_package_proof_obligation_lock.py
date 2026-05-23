import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_proof_obligation_lock_status_and_next_object():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_proof_obligation_lock_2026_05_23.json").read_text())
    assert data["status"] == "PROOF_OBLIGATION_LOCK_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["previous_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_BRIDGE"
    assert data["next_admissible_object"] == "LOCAL_BALANCE_LAW_DQDT_DERIVATION"

def test_proof_obligation_lock_records_remaining_next_admissible_objects():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_proof_obligation_lock_2026_05_23.json").read_text())
    expected = [
        "LOCAL_BALANCE_LAW_DQDT_DERIVATION",
        "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF",
        "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF",
        "PACKAGE_COMPATIBILITY_PROOF",
        "TARGET_INTERFACE_COMPATIBILITY_PROOF",
        "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF",
    ]
    assert data["remaining_next_admissible_objects"] == expected

def test_proof_obligation_lock_preserves_boundaries():
    data = json.loads((ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_proof_obligation_lock_2026_05_23.json").read_text())
    for token in [
        "no local balance law dQ/dt derivation",
        "no restricted concentration monotonicity proof",
        "no restricted continuation norm control proof",
        "no package compatibility proof",
        "no target-interface compatibility proof",
        "no concrete analytic Einstein-matter estimate package proof",
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]:
        assert token in data["boundary"]

def test_proof_obligation_lock_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLock.lean").read_text()
    for token in [
        "ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLockData",
        "ConcreteAnalyticEinsteinMatterEstimatePackageProofObligationLockHypotheses",
        "localBalanceLawDQDTDerivation",
        "restrictedConcentrationMonotonicityProof",
        "restrictedContinuationNormControlProof",
        "packageCompatibilityProof",
        "targetInterfaceCompatibilityProof",
        "concreteAnalyticEstimatePackageProof",
    ]:
        assert token in text
