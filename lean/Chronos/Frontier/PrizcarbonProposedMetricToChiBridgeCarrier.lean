import Chronos.Frontier.PrizcarbonR3CompactVariationalWitness
import Chronos.Frontier.PrizcarbonProposedScalarFirstVariationIBP

namespace Chronos.Frontier

noncomputable section

/--
A proposed bridge carrier between the metric-derived odd-parity radial master
profile and a candidate Prizcarbon pseudoscalar radial profile.

The carrier records a relation between functions `ℝ → ℝ`. It does not require
equality, equivalence, injectivity, surjectivity, or an inverse map.
-/
structure ProposedPrizcarbonMetricToChiBridgeCarrier where
  chiCandidate :
    ReggeWheelerOddParityRadialJet → ℝ → ℝ
  bridgeRelation :
    (ℝ → ℝ) → (ℝ → ℝ) → Prop
  bridgeWitness :
    ∀ rawState : ReggeWheelerOddParityRadialJet,
      bridgeRelation
        (reggeWheelerOddParityMasterField rawState)
        (chiCandidate rawState)
  chiGaugeInvariant :
    ∀ (rawState : ReggeWheelerOddParityRadialJet)
      (gaugeParameter : ReggeWheelerOddParityGaugeJet),
      chiCandidate
          (reggeWheelerOddParityGaugeTransform
            rawState gaugeParameter) =
        chiCandidate rawState

theorem proposedPrizcarbon_metricToChiBridge_relation
    (carrier : ProposedPrizcarbonMetricToChiBridgeCarrier)
    (rawState : ReggeWheelerOddParityRadialJet) :
    carrier.bridgeRelation
      (reggeWheelerOddParityMasterField rawState)
      (carrier.chiCandidate rawState) :=
  carrier.bridgeWitness rawState

theorem proposedPrizcarbon_metricToChiBridge_pairGaugeInvariant
    (carrier : ProposedPrizcarbonMetricToChiBridgeCarrier)
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    reggeWheelerOddParityMasterField
          (reggeWheelerOddParityGaugeTransform
            rawState gaugeParameter) =
        reggeWheelerOddParityMasterField rawState ∧
      carrier.chiCandidate
          (reggeWheelerOddParityGaugeTransform
            rawState gaugeParameter) =
        carrier.chiCandidate rawState := by
  exact ⟨
    reggeWheelerOddParityMasterField_gaugeInvariant
      rawState gaugeParameter,
    carrier.chiGaugeInvariant rawState gaugeParameter
  ⟩

theorem proposedPrizcarbon_metricToChiBridge_relation_gaugeTransform
    (carrier : ProposedPrizcarbonMetricToChiBridgeCarrier)
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    carrier.bridgeRelation
      (reggeWheelerOddParityMasterField
        (reggeWheelerOddParityGaugeTransform
          rawState gaugeParameter))
      (carrier.chiCandidate
        (reggeWheelerOddParityGaugeTransform
          rawState gaugeParameter)) := by
  rw [
    reggeWheelerOddParityMasterField_gaugeInvariant
      rawState gaugeParameter,
    carrier.chiGaugeInvariant rawState gaugeParameter
  ]
  exact carrier.bridgeWitness rawState

end

end Chronos.Frontier

namespace Chronos.Frontier

noncomputable section

/--
A concrete candidate chi profile obtained by multiplying the gauge-invariant
metric master profile by the radial coordinate.

This is an explicit radial-weight ansatz, not a derivation from the proposed
covariant action.
-/
def proposedPrizcarbonRadialWeightedChiCandidate
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ → ℝ :=
  fun radius =>
    radius *
      reggeWheelerOddParityMasterField rawState radius

/--
The candidate chi profile is related to the metric master profile by radial
weighting. This relation does not assert that the two profiles are equal.
-/
def proposedPrizcarbonRadialWeightedBridgeRelation
    (metricProfile chiProfile : ℝ → ℝ) : Prop :=
  ∀ radius : ℝ,
    chiProfile radius =
      radius * metricProfile radius

theorem proposedPrizcarbon_radialWeightedBridge_witness
    (rawState : ReggeWheelerOddParityRadialJet) :
    proposedPrizcarbonRadialWeightedBridgeRelation
      (reggeWheelerOddParityMasterField rawState)
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) := by
  intro radius
  rfl

theorem proposedPrizcarbon_radialWeightedChi_gaugeInvariant
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    proposedPrizcarbonRadialWeightedChiCandidate
        (reggeWheelerOddParityGaugeTransform
          rawState gaugeParameter) =
      proposedPrizcarbonRadialWeightedChiCandidate
        rawState := by
  funext radius
  unfold proposedPrizcarbonRadialWeightedChiCandidate
  rw [
    reggeWheelerOddParityMasterField_gaugeInvariant
      rawState gaugeParameter
  ]

def proposedPrizcarbonRadialWeightedBridgeCarrier :
    ProposedPrizcarbonMetricToChiBridgeCarrier :=
  {
    chiCandidate :=
      proposedPrizcarbonRadialWeightedChiCandidate
    bridgeRelation :=
      proposedPrizcarbonRadialWeightedBridgeRelation
    bridgeWitness :=
      proposedPrizcarbon_radialWeightedBridge_witness
    chiGaugeInvariant :=
      proposedPrizcarbon_radialWeightedChi_gaugeInvariant
  }

theorem proposedPrizcarbon_radialWeightedBridgeCarrier_relation
    (rawState : ReggeWheelerOddParityRadialJet) :
    proposedPrizcarbonRadialWeightedBridgeCarrier.bridgeRelation
      (reggeWheelerOddParityMasterField rawState)
      (proposedPrizcarbonRadialWeightedBridgeCarrier.chiCandidate
        rawState) :=
  proposedPrizcarbon_metricToChiBridge_relation
    proposedPrizcarbonRadialWeightedBridgeCarrier
    rawState

/--
The radial-weighted relation genuinely permits distinct profiles, so the
carrier does not silently collapse its relation into profile equality.
-/
theorem proposedPrizcarbon_radialWeightedRelation_permitsDistinctProfiles :
    ∃ metricProfile chiProfile : ℝ → ℝ,
      proposedPrizcarbonRadialWeightedBridgeRelation
          metricProfile chiProfile ∧
        chiProfile ≠ metricProfile := by
  refine ⟨fun _ => 1, fun radius => radius, ?_, ?_⟩
  · unfold proposedPrizcarbonRadialWeightedBridgeRelation
    intro radius
    simp
  · intro hEquality
    have hAtZero := congrFun hEquality 0
    norm_num at hAtZero

end

end Chronos.Frontier
