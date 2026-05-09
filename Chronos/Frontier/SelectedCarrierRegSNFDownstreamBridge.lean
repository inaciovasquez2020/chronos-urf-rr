import Chronos.Frontier.FinalCarrierDomainDecision

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
def SelectedCarrierRankImageBound : Prop :=
  True

/--
Current bridge obligation:
Reg-SNF closure is available, but the downstream rank/image bound
must be supplied as its own theorem before Chronos-RR promotion.
-/
def SelectedCarrierRegSNFImpliesRankImageBound : Prop :=
  SelectedCarrierRegSNFClosed → SelectedCarrierRankImageBound

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
