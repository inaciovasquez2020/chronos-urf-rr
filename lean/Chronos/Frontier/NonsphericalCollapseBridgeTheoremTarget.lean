import Chronos.Frontier.QuasiLocalCollapseGateConditionalBridge

namespace Chronos
namespace Frontier

def NonsphericalCollapseBridgeTheoremTarget : Prop :=
  ∀ I : QuasiLocalCollapseGateInput,
    QuasiLocalCollapseGateCondition I →
    MarginalOrTrappedNullExpansionSurface I

theorem nonspherical_collapse_bridge_theorem_target_matches_missing_object :
    NonsphericalCollapseBridgeTheoremTarget = NonsphericalCollapseBridgeLemma := by
  rfl

def nonsphericalCollapseBridgeTheoremTargetStatus : String :=
  "OPEN_PROBLEM_REQUIRED"

def nonsphericalCollapseBridgeTheoremTargetBoundary : String :=
  "THEOREM_TARGET_ONLY_NOT_PROVED"

def nonsphericalCollapseBridgeTheoremTargetWeakestMissingObject : String :=
  "NonsphericalCollapseBridgeTheoremTarget"

end Frontier
end Chronos
