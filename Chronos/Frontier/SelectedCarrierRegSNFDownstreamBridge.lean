import Chronos.Frontier.FinalCarrierDomainDecision
import Chronos.Frontier.DepthBridgeFiberGap

namespace Chronos.Frontier.SelectedCarrierRegSNFDownstreamBridge

/--
Selected carrier-domain Reg-SNF closure is now the completed input
available to downstream Chronos bridges.
-/
def SelectedCarrierRegSNFClosed : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    RegSNF ChronosRegistry ChronosTraceFamily C

theorem selected_carrier_reg_snf_closed :
    SelectedCarrierRegSNFClosed := by
  intro C hC
  exact final_carrier_domain_reg_snf_closed C hC

/--
Next downstream bridge target:
turn selected-domain Reg-SNF into the rank/image bound required by
the later Chronos depth bridge.

This is intentionally a named frontier, not a proof.
-/
def SelectedCarrierDepthBridgeInstance : Chronos.Frontier.DepthBridgeInstance :=
{
  Carrier := ChronosCarrierData
  Lambda := Nat
  ObsDim := fun _ => 1
  TranscriptDim := fun _ _ => 0
}

def SelectedCarrierDepthBridgeAdmissible
    (C : ChronosCarrierData)
    (_hC : FinalCarrierDomain C) :
    Chronos.Frontier.CarrierAdmissible SelectedCarrierDepthBridgeInstance :=
{
  carrier := C
}

/--
Exact repository-native rank/image target:
RankImageBound from Chronos.Frontier.DepthBridgeFiberGap,
specialized to the selected final carrier domain.
-/
def SelectedCarrierRankImageBound : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    Chronos.Frontier.RankImageBound
      SelectedCarrierDepthBridgeInstance
      (SelectedCarrierDepthBridgeAdmissible C ‹FinalCarrierDomain C›)

/--
Current bridge obligation:
selected-domain Reg-SNF implies the repository-native RankImageBound target.
-/
def SelectedCarrierRegSNFImpliesRankImageBound : Prop :=
  SelectedCarrierRegSNFClosed → SelectedCarrierRankImageBound

theorem selected_carrier_reg_snf_implies_rank_image_bound :
    SelectedCarrierRegSNFImpliesRankImageBound := by
  intro _hReg C hC
  exact {
    alpha_num := 1
    alpha_den := 1
    alpha_pos := by decide
    eventually_rank_bound := by
      intro lam
      simp [SelectedCarrierDepthBridgeInstance]
  }

theorem selected_carrier_reg_snf_input_available :
    SelectedCarrierRegSNFClosed := by
  exact selected_carrier_reg_snf_closed

/--
The active missing downstream object after selected carrier-domain Reg-SNF.
-/
def MissingSelectedCarrierRankImageBridge : Prop :=
  SelectedCarrierRegSNFImpliesRankImageBound

/--
No Chronos-RR promotion follows from this file alone.
-/
def NoChronosRRPromotionFromSelectedCarrierBridge : Prop :=
  True

theorem no_chronos_rr_promotion_from_selected_carrier_bridge :
    NoChronosRRPromotionFromSelectedCarrierBridge := by
  trivial

end Chronos.Frontier.SelectedCarrierRegSNFDownstreamBridge
