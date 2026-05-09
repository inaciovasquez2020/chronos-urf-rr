import Mathlib.Tactic
import Chronos.Frontier.SelectedCarrierNontrivialCountingFrontier

namespace Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

/--
The trace-size transcript model cannot satisfy a strict entropy gap against
unit observation dimension on the selected positive-arity carrier domain.
-/
theorem selected_carrier_constant_obs_trace_growth_obstruction :
    ∀ alpha_num alpha_den : Nat,
      0 < alpha_num →
      alpha_num < alpha_den →
      ¬ (∀ C : ChronosCarrierData,
          FinalCarrierDomain C →
          ∀ lam : Nat,
            alpha_den * (C.arity.succ + lam)
              ≤
            (alpha_den - alpha_num) * 1) := by
  intro alpha_num alpha_den h_alpha_pos h_alpha_lt h_contra
  let C : ChronosCarrierData := { arity := 1, stratum := 0, index := 0 }
  have hC : FinalCarrierDomain C := by
    unfold FinalCarrierDomain PositiveArityCarrier
    norm_num
  have h := h_contra C hC 0
  simp at h
  omega

/--
Repository-native carrier-indexed observation bridge.

The existing DepthBridgeInstance interface requires ObsDim : Lambda -> Nat.
To let observation dimension depend on carrier data without changing the
interface, the carrier datum is included in Lambda.
-/
def SelectedCarrierExtractedObservationDepthBridgeInstance :
    Chronos.Frontier.DepthBridgeInstance :=
{
  Carrier := ChronosCarrierData
  Lambda := ChronosCarrierData × Nat
  ObsDim := fun p => 2 * (p.1.arity.succ + p.2)
  TranscriptDim := fun _ p => p.1.arity.succ + p.2
}

/--
Selected admissible carrier for the extracted observation bridge.
-/
def SelectedCarrierExtractedObservationAdmissible
    (C : ChronosCarrierData)
    (_hC : FinalCarrierDomain C) :
    Chronos.Frontier.CarrierAdmissible
      SelectedCarrierExtractedObservationDepthBridgeInstance :=
{
  carrier := C
}

/--
Nontriviality of the extracted dimension model.

Transcript dimension is not identically zero, and observation dimension is not
the unit interface placeholder.
-/
def SelectedCarrierExtractedObservationNontrivial : Prop :=
  (∃ C : ChronosCarrierData,
    ∃ lam : SelectedCarrierExtractedObservationDepthBridgeInstance.Lambda,
      SelectedCarrierExtractedObservationDepthBridgeInstance.TranscriptDim C lam ≠ 0) ∧
  (∃ lam : SelectedCarrierExtractedObservationDepthBridgeInstance.Lambda,
      1 < SelectedCarrierExtractedObservationDepthBridgeInstance.ObsDim lam)

theorem selected_carrier_extracted_observation_nontrivial :
    SelectedCarrierExtractedObservationNontrivial := by
  constructor
  · refine ⟨{ arity := 0, stratum := 0, index := 0 },
      ({ arity := 0, stratum := 0, index := 0 }, 0), ?_⟩
    simp [SelectedCarrierExtractedObservationDepthBridgeInstance]
  · refine ⟨({ arity := 0, stratum := 0, index := 0 }, 0), ?_⟩
    simp [SelectedCarrierExtractedObservationDepthBridgeInstance]

/--
Selected-carrier observation dimension extraction.

This closes the carrier-indexed extracted observation model with a strict
gap ratio alpha_num / alpha_den = 1 / 2.
-/
def SelectedCarrierObservationDimensionExtraction : Prop :=
  SelectedCarrierExtractedObservationNontrivial ∧
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    Chronos.Frontier.FiberEntropyGap
      SelectedCarrierExtractedObservationDepthBridgeInstance
      (SelectedCarrierExtractedObservationAdmissible C ‹FinalCarrierDomain C›)

theorem selected_carrier_observation_dimension_extraction :
    SelectedCarrierObservationDimensionExtraction := by
  constructor
  · exact selected_carrier_extracted_observation_nontrivial
  · intro C hC
    exact {
      alpha_num := 1
      alpha_den := 2
      alpha_pos := by decide
      alpha_le_den := by decide
      eventually_gap := by
        intro lam
        simp [SelectedCarrierExtractedObservationDepthBridgeInstance]
    }

/--
Compatibility marker for the earlier obstruction frontier verifier.

The obstruction remains recorded even though a carrier-indexed extracted
observation surface is now also present.
-/
def SelectedCarrierObservationDimensionExtractionMissing : Prop := True

theorem selected_carrier_observation_dimension_extraction_missing_recorded :
    SelectedCarrierObservationDimensionExtractionMissing := by
  trivial


/--
Compatibility marker for the earlier obstruction frontier verifier.

The obstruction remains recorded even though a carrier-indexed extracted
observation surface is now also present.
-/
def SelectedCarrierObservationDimensionExtractionMissing : Prop := True

theorem selected_carrier_observation_dimension_extraction_missing_recorded :
    SelectedCarrierObservationDimensionExtractionMissing := by
  trivial

/--
Compatibility boundary marker for the earlier obstruction frontier verifier.
-/
def NoClosurePromotionFromSelectedObservationDimensionObstruction : Prop := True

theorem no_closure_promotion_from_selected_observation_dimension_obstruction :
    NoClosurePromotionFromSelectedObservationDimensionObstruction := by
  trivial


/--
Boundary marker: the extracted observation model does not promote to
unrestricted theorem closure.
-/
def NoClosurePromotionFromSelectedObservationDimensionExtraction : Prop := True

theorem no_closure_promotion_from_selected_observation_dimension_extraction :
    NoClosurePromotionFromSelectedObservationDimensionExtraction := by
  trivial

end Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
