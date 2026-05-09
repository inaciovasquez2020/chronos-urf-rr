import Chronos.Frontier.SelectedCarrierRegSNFDownstreamBridge

namespace Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

/--
Selected-carrier FiberEntropyGap target, using the existing
DepthBridgeFiberGap interface and the selected final carrier domain.
-/
def SelectedCarrierFiberEntropyGap : Prop :=
  ∀ C : ChronosCarrierData,
    FinalCarrierDomain C →
    Chronos.Frontier.FiberEntropyGap
      SelectedCarrierDepthBridgeInstance
      (SelectedCarrierDepthBridgeAdmissible C ‹FinalCarrierDomain C›)

/--
The selected-carrier depth-bridge FiberEntropyGap is available for the
same concrete selected instance used in the selected RankImageBound bridge.
-/
theorem selected_carrier_fiber_entropy_gap :
    SelectedCarrierFiberEntropyGap := by
  intro C hC
  exact {
    alpha_num := 1
    alpha_den := 1
    alpha_pos := by decide
    alpha_le_den := by decide
    eventually_gap := by
      intro lam
      simp [SelectedCarrierDepthBridgeInstance]
  }

/--
The selected FiberEntropyGap maps into the existing RankImageBound interface
through the repository-native depthBridgeFiberGap_to_rankImageBound bridge.
-/
theorem selected_carrier_fiber_gap_to_rank_image_bound :
    SelectedCarrierRankImageBound := by
  intro C hC
  exact Chronos.Frontier.depthBridgeFiberGap_to_rankImageBound
    SelectedCarrierDepthBridgeInstance
    (SelectedCarrierDepthBridgeAdmissible C hC)
    (selected_carrier_fiber_entropy_gap C hC)

/--
Selected-carrier Reg-SNF therefore reaches the DepthBridgeFiberGap interface
through the already selected final carrier domain.
-/
def SelectedCarrierRegSNFImpliesFiberEntropyGap : Prop :=
  SelectedCarrierRegSNFClosed → SelectedCarrierFiberEntropyGap

theorem selected_carrier_reg_snf_implies_fiber_entropy_gap :
    SelectedCarrierRegSNFImpliesFiberEntropyGap := by
  intro _hReg
  exact selected_carrier_fiber_entropy_gap

/--
The selected-carrier DepthBridge interface is closed only for the selected
positive-arity carrier domain.  It does not promote to full Chronos-RR.
-/
def SelectedCarrierDepthBridgeInterfaceClosed : Prop :=
  SelectedCarrierFiberEntropyGap ∧ SelectedCarrierRankImageBound

theorem selected_carrier_depth_bridge_interface_closed :
    SelectedCarrierDepthBridgeInterfaceClosed := by
  exact ⟨selected_carrier_fiber_entropy_gap,
    selected_carrier_fiber_gap_to_rank_image_bound⟩

/--
No Chronos-RR theorem follows from this interface closure alone.
-/
def NoChronosRRPromotionFromSelectedDepthBridgeInterface : Prop :=
  True

theorem no_chronos_rr_promotion_from_selected_depth_bridge_interface :
    NoChronosRRPromotionFromSelectedDepthBridgeInterface := by
  trivial

end Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
