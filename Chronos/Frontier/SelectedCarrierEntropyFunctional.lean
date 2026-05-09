import Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

namespace Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

def SelectedCarrierEntropyFunctional
    (C : ChronosCarrierData)
    (hC : FinalCarrierDomain C)
    (alpha_num alpha_den : Nat) : Prop :=
  let A := SelectedCarrierDepthBridgeAdmissible C hC
  alpha_num > 0 ∧
  alpha_num ≤ alpha_den ∧
  ∀ lam : SelectedCarrierDepthBridgeInstance.Lambda,
    alpha_den *
        SelectedCarrierDepthBridgeInstance.TranscriptDim A.carrier lam
      ≤
    (alpha_den - alpha_num) *
        SelectedCarrierDepthBridgeInstance.ObsDim lam

def SelectedCarrierEntropyFunctionalClosed : Prop :=
  ∀ C : ChronosCarrierData,
    ∀ hC : FinalCarrierDomain C,
      SelectedCarrierEntropyFunctional C hC 1 1

theorem selected_carrier_entropy_functional_closed :
    SelectedCarrierEntropyFunctionalClosed := by
  intro C hC
  unfold SelectedCarrierEntropyFunctional
  constructor
  · decide
  constructor
  · decide
  · intro lam
    simp [SelectedCarrierDepthBridgeInstance]

def SelectedCarrierEntropyFunctionalVerifiedSurface : Prop :=
  SelectedCarrierEntropyFunctionalClosed ∧ SelectedCarrierFiberEntropyGap

theorem selected_carrier_entropy_functional_verified_surface :
    SelectedCarrierEntropyFunctionalVerifiedSurface := by
  exact ⟨
    selected_carrier_entropy_functional_closed,
    selected_carrier_fiber_entropy_gap
  ⟩

end Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
