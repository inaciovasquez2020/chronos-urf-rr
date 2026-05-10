import Chronos.Frontier.H4_1_FGL_Bridge1Refutation
import Chronos.Frontier.SelectedCarrierEntropyFunctional
import Chronos.Frontier.FinalCarrierDomainDecision
import Chronos.Frontier.IntendedChronosAdmissibility

namespace Chronos.Frontier.H4_1_FGL_RestrictedDomainReduction

open Chronos.Frontier.H4_1_FGL_Bridge1Refutation
open Chronos.Frontier.FinalCarrierDomainDecision
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

theorem h4_1_fgl_unrestricted_bridge1_refuted :
    ¬ H4_1_FGL_AdmissibleToFinalCarrierDomain := by
  exact admissible_to_final_carrier_domain_false

def H4_1_FGL_FinalCarrierDomainTarget : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    UniversalFiberEntropyGap C

def H4_1_FGL_FinalCarrierSelectedGapSoundness : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    SelectedCarrierFiberEntropyGap →
    UniversalFiberEntropyGap C

theorem h4_1_fgl_final_domain_reduction :
    H4_1_FGL_FinalCarrierSelectedGapSoundness →
    H4_1_FGL_FinalCarrierDomainTarget := by
  intro h_sound C hC
  have hS : SelectedCarrierFiberEntropyGap :=
    selected_carrier_entropy_functional_verified_surface C hC
  exact h_sound C hC hS

def H4_1_FGL_IntendedCarrierTarget : Prop :=
  ∀ C : ChronosCarrierData,
    IntendedChronosCarrier C →
    UniversalFiberEntropyGap C

def H4_1_FGL_IntendedToFinalCarrierDomain : Prop :=
  ∀ C : ChronosCarrierData,
    IntendedChronosCarrier C →
    FinalCarrierDomain C

theorem h4_1_fgl_intended_domain_reduction :
    H4_1_FGL_IntendedToFinalCarrierDomain →
    H4_1_FGL_FinalCarrierDomainTarget →
    H4_1_FGL_IntendedCarrierTarget := by
  intro h_intended_final h_final C hC
  exact h_final C (h_intended_final C hC)

def H4_1_FGL_RestrictedDomainStatus : String :=
  "RESTRICTED_DOMAIN_REDUCTION_ONLY / ZERO_ARITY_COUNTEREXAMPLE_RECORDED / UNIVERSAL_SOUNDNESS_FRONTIER_OPEN"

theorem h4_1_fgl_restricted_domain_status_record :
    H4_1_FGL_RestrictedDomainStatus =
      "RESTRICTED_DOMAIN_REDUCTION_ONLY / ZERO_ARITY_COUNTEREXAMPLE_RECORDED / UNIVERSAL_SOUNDNESS_FRONTIER_OPEN" := by
  rfl

end Chronos.Frontier.H4_1_FGL_RestrictedDomainReduction
