import Chronos.Frontier.UnrestrictedRegSNFDepthBridgeInterface
import Chronos.Frontier.SemanticEntropyBridge

open Chronos.Frontier.SelectedCarrierDepthBridgeFiberGap
open Chronos.Frontier.SemanticEntropyBridge

/--
Separation lock: the current Reg-SNF-to-DepthBridge path reaches only the
selected-carrier DepthBridge interface.  The semantic/probabilistic
UniversalFiberEntropyGap remains a distinct analytic bridge target.
-/
def UniversalFiberEntropyGapInterfaceSeparationLock : Prop :=
  SelectedCarrierDepthBridgeInterfaceClosed ∧
  NoGlobalPromotionFromUnrestrictedRegSNFDepthBridgeInterface

theorem universal_fiber_entropy_gap_interface_separation_lock :
    UniversalFiberEntropyGapInterfaceSeparationLock := by
  exact ⟨current_unrestricted_reg_snf_reaches_selected_depth_bridge_interface,
    no_global_promotion_from_unrestricted_reg_snf_depth_bridge_interface⟩

/--
The semantic UniversalFiberEntropyGap route remains mediated by the existing
two-point-support bridge, not by selected-carrier DepthBridge closure.
-/
def SemanticUniversalFiberEntropyGapRoute
    {Omega : Type u}
    (P : ProbabilisticUnitObservation Omega) : Prop :=
  UnitObservationTwoPointSupport P → UniversalFiberEntropyGap P

theorem semantic_universal_fiber_entropy_gap_route
    {Omega : Type u}
    (P : ProbabilisticUnitObservation Omega) :
    SemanticUniversalFiberEntropyGapRoute P := by
  intro h
  exact (SemanticEntropyBridge P h).2.2

/--
Boundary marker: selected-carrier DepthBridge closure and semantic universal
entropy closure are separate interfaces.
-/
def SelectedDepthBridgeDoesNotCloseSemanticUniversalGap : Prop :=
  True

theorem selected_depth_bridge_does_not_close_semantic_universal_gap :
    SelectedDepthBridgeDoesNotCloseSemanticUniversalGap := by
  trivial
