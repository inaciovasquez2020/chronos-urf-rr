import Chronos.Frontier.H4_1_FGL_RestrictedDomainReduction
import Chronos.Frontier.UniversalFiberEntropyGapSeparationLock
import Chronos.Frontier.UniversalFiberEntropyGapWitnessInterface

namespace Chronos.Frontier.H4_1_FGL_FinalSoundnessFrontier

open Chronos.Frontier.H4_1_FGL_RestrictedDomainReduction
open Chronos.Frontier.FinalCarrierDomainDecision
open Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
open Chronos.Frontier.SemanticEntropyBridge
open Chronos.Frontier.UniversalFiberEntropyGapWitnessInterface

def H4_1_FGL_FinalCarrierSelectedGapSoundnessFrontier : Prop :=
  H4_1_FGL_FinalCarrierSelectedGapSoundness

def H4_1_FGL_SelectedDepthBridgeSemanticSeparation : Prop :=
  UniversalFiberEntropyGapInterfaceSeparationLock ∧
  SelectedDepthBridgeDoesNotCloseSemanticUniversalGap

theorem h4_1_fgl_selected_depth_bridge_semantic_separation :
    H4_1_FGL_SelectedDepthBridgeSemanticSeparation := by
  exact ⟨
    universal_fiber_entropy_gap_interface_separation_lock,
    selected_depth_bridge_does_not_close_semantic_universal_gap
  ⟩

def H4_1_FGL_FinalCarrierObservationExtraction : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    ∃ (Omega : Type) (P : ProbabilisticUnitObservation Omega),
      UnitObservationTwoPointSupport P

theorem h4_1_fgl_observation_extraction_to_semantic_gap :
    H4_1_FGL_FinalCarrierObservationExtraction →
    ∀ C : ChronosCarrierData,
      FinalCarrierDomain C →
      ∃ (Omega : Type) (P : ProbabilisticUnitObservation Omega),
        UniversalFiberEntropyGap P := by
  intro h_extract C hC
  rcases h_extract C hC with ⟨Omega, P, h_two⟩
  exact ⟨Omega, P, universal_fiber_entropy_gap_witness_interface P h_two⟩

def H4_1_FGL_FinalSoundnessStatus : String :=
  "FRONTIER_OPEN / FINAL_CARRIER_SELECTED_GAP_SOUNDNESS_REQUIRES_OBSERVATION_EXTRACTION"

theorem h4_1_fgl_final_soundness_status_record :
    H4_1_FGL_FinalSoundnessStatus =
      "FRONTIER_OPEN / FINAL_CARRIER_SELECTED_GAP_SOUNDNESS_REQUIRES_OBSERVATION_EXTRACTION" := by
  rfl

end Chronos.Frontier.H4_1_FGL_FinalSoundnessFrontier
