#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/analytic_estimate_candidate_packet_2026_05_23.json"
STATUS = ROOT / "docs/status/ANALYTIC_ESTIMATE_CANDIDATE_PACKET_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/AnalyticEstimateCandidatePacket.lean"

CANDIDATES = [
    "SemiclassicalEinsteinKGFixedPointTemplate",
    "MaxwellBoltzmannBianchiMatterWellPosednessTemplate",
    "ActiveLiquidCrystalBootstrapEnergyTemplate",
    "TSIMFGRPDEFurtherLiteratureTargets",
    "LeanSearchPremiseRetrievalSupport",
    "StatisticalHypothesisTestingEmpiricalAuditSupport",
    "StatisticalFieldTheoryBackgroundSupport",
    "KOTheoreticGravityBackgroundSupport",
    "TotalityTheoremClaimBoundaryBackground",
    "ConcreteSixFieldSlotEstimateGap",
]

UNFILLED_SLOTS = [
    "localExistenceSlot",
    "localUniquenessSlot",
    "constraintPropagationSlot",
    "gaugeControlSlot",
    "energyBootstrapSlot",
    "refinedEnergyEstimateSlot",
    "matterCouplingControlSlot",
    "energyConditionPreservationSlot",
    "nonsymmetricPersistenceSlot",
    "concentrationTransportSlot",
    "continuationAlternativeSlot",
    "collapseThresholdCriterionSlot",
    "collapseGateTriggerSlot",
    "slabIterationSlot",
    "sixFieldInstantiationSlot",
]

BLOCKED = [
    "proof of SixFieldAnalyticPackageHypothesis",
    "proof of NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "proof of Einstein-matter well-posedness",
    "proof of non-symmetric persistence",
    "proof of matter-coupling control",
    "proof of concentration transport",
    "proof of collapse-gate trigger",
    "proof of cosmic censorship",
    "proof of hoop conjecture",
    "proof of gravity closure",
    "proof of Chronos-RR",
    "proof of H4.1/FGL",
    "proof of P vs NP",
    "proof of any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "ANALYTIC_ESTIMATE_CANDIDATE_PACKET"
    assert data["status"] == "CANDIDATE_PACKET_ONLY_NO_ANALYTIC_ESTIMATE_PROOF"
    assert data["candidate_count"] == 10
    assert len(data["candidates"]) == 10
    assert data["next_admissible_object"] == "FilledConcreteInitialDataClass"

    names = [item["name"] for item in data["candidates"]]
    assert names == CANDIDATES

    for item in data["candidates"]:
        assert item["proof_supplied"] is False
        assert item["status"] in {"CANDIDATE_ONLY", "OPEN_GAP"}

    for name in CANDIDATES:
        assert name in status, name
        assert name in lean, name

    for slot in UNFILLED_SLOTS:
        assert slot in data["unfilled_slots_after_packet"], slot
        assert slot in status, slot

    for phrase in BLOCKED:
        assert phrase in data["blocked_use"], phrase
        assert phrase in status, phrase

    assert "analytic_estimate_candidate_name_count" in lean
    assert "analytic_estimate_candidate_count" in lean
    assert "analytic_estimate_candidate_packet_does_not_prove_six_field" in lean
    assert "analytic_estimate_candidate_packet_does_not_prove_gravity_closure" in lean

    print("Analytic estimate candidate packet verification OK.")
    print("Status:", data["status"])
    print("Candidate count:", data["candidate_count"])
    print("Next admissible object:", data["next_admissible_object"])

if __name__ == "__main__":
    main()
