#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/remaining_six_field_proof_obligations_registry_2026_05_23.json"
STATUS = ROOT / "docs/status/REMAINING_SIX_FIELD_PROOF_OBLIGATIONS_REGISTRY_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/RemainingSixFieldProofObligationsRegistry.lean"

OBLIGATIONS = [
    "AnalyticEstimateCandidatePacket",
    "FilledConcreteInitialDataClass",
    "FilledConcreteMatterModel",
    "LocalExistenceProof",
    "LocalUniquenessProof",
    "ConstraintPropagationProof",
    "GaugeControlProof",
    "EnergyBootstrapProof",
    "RefinedEnergyEstimateProof",
    "BootstrapClosureProof",
    "MatterCouplingControlProof",
    "EnergyConditionPreservationProof",
    "NonSymmetricPersistenceProof",
    "ConcentrationTransportProof",
    "ContinuationAlternativeProof",
    "CollapseThresholdCriterionProof",
    "CollapseGateTriggerProof",
    "SlabIterationProof",
    "BootstrapSlabToSixFieldInstantiationProof",
    "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackageProof",
    "SixFieldAnalyticPackageHypothesisProof",
    "RestrictedGravityClosureBridgeProof",
]

BLOCKED = [
    "proof of SixFieldAnalyticPackageHypothesis",
    "proof of NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "proof of Einstein-matter well-posedness",
    "proof of non-symmetric collapse",
    "proof of cosmic censorship",
    "proof of hoop conjecture",
    "proof of gravity closure",
    "proof of Chronos-RR",
    "proof of H4.1/FGL",
    "proof of P vs NP",
    "proof of any Clay problem",
]

STILL_NOT_PROVED = [
    "unrestricted Einstein-matter well-posedness",
    "unrestricted non-symmetric collapse theorem",
    "cosmic censorship",
    "hoop conjecture",
    "unrestricted gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "REMAINING_SIX_FIELD_PROOF_OBLIGATIONS_REGISTRY"
    assert data["status"] == "OPEN_PROOF_OBLIGATION_REGISTRY_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["obligation_count"] == 22
    assert len(data["obligations"]) == 22
    assert data["next_admissible_object"] == "AnalyticEstimateCandidatePacket"

    names = [item["name"] for item in data["obligations"]]
    assert names == OBLIGATIONS

    for item in data["obligations"]:
        assert item["status"] == "OPEN"

    for name in OBLIGATIONS:
        assert name in status, name
        assert name in lean, name

    for phrase in STILL_NOT_PROVED:
        assert phrase in data["still_not_proved"], phrase
        assert phrase in status, phrase

    for phrase in BLOCKED:
        assert phrase in data["blocked_use"], phrase
        assert phrase in status, phrase

    assert "remaining_six_field_proof_obligation_count" in lean
    assert "remaining_six_field_proof_obligations_count" in lean
    assert "remaining_registry_does_not_prove_six_field" in lean
    assert "remaining_registry_does_not_prove_gravity_closure" in lean

    print("Remaining six-field proof obligations registry verification OK.")
    print("Status:", data["status"])
    print("Obligation count:", data["obligation_count"])
    print("Next admissible object:", data["next_admissible_object"])

if __name__ == "__main__":
    main()
