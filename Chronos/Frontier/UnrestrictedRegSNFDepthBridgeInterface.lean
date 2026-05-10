import Chronos.Frontier.RepresentedZeroArityRegSNFClosure
import Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.RealChronosAdmissible
open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap

/--
The unrestricted Reg-SNF closure over the current real Chronos-admissible
predicate reaches the existing selected-carrier DepthBridge interface.
This does not extend the DepthBridge interface beyond its selected domain.
-/
def UnrestrictedRegSNFReachesSelectedDepthBridgeInterface : Prop :=
  (∀ C : ChronosCarrierData,
      RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C →
      RegSNF ChronosRegistry ChronosTraceFamily C) →
    SelectedCarrierDepthBridgeInterfaceClosed

theorem unrestricted_reg_snf_reaches_selected_depth_bridge_interface :
    UnrestrictedRegSNFReachesSelectedDepthBridgeInterface := by
  intro _hReg
  exact selected_carrier_depth_bridge_interface_closed

/--
Concrete instantiated version using the merged unrestricted Reg-SNF closure.
-/
theorem current_unrestricted_reg_snf_reaches_selected_depth_bridge_interface :
    SelectedCarrierDepthBridgeInterfaceClosed := by
  exact unrestricted_reg_snf_reaches_selected_depth_bridge_interface
    unrestricted_real_chronos_admissible_reg_snf_closed

/--
Boundary lock: selected DepthBridge interface closure does not promote to
Chronos-RR or any global theorem beyond the selected interface.
-/
def NoGlobalPromotionFromUnrestrictedRegSNFDepthBridgeInterface : Prop :=
  NoChronosRRPromotionFromSelectedDepthBridgeInterface

theorem no_global_promotion_from_unrestricted_reg_snf_depth_bridge_interface :
    NoGlobalPromotionFromUnrestrictedRegSNFDepthBridgeInterface := by
  exact no_chronos_rr_promotion_from_selected_depth_bridge_interface
