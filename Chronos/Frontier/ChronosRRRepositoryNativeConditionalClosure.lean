import Chronos.Frontier.DepthBridgeFromRepositoryNativeUniversalGap

namespace Chronos.Frontier

/--
Repository-native Chronos-RR conditional closure surface.

This is not unrestricted Chronos-RR. It records only the repository-native
conditional closure obtained once the repository-native depth-bridge witness
surface is available.
-/
def RepositoryNativeChronosRRConditionalClosure : Prop :=
  RepositoryNativeDepthBridgeWitness

theorem repository_native_chronos_rr_conditional_closure_from_depth_bridge
    (h : RepositoryNativeDepthBridgeWitness) :
    RepositoryNativeChronosRRConditionalClosure := by
  exact h

theorem canonical_repository_native_chronos_rr_conditional_closure :
    RepositoryNativeChronosRRConditionalClosure := by
  exact repository_native_chronos_rr_conditional_closure_from_depth_bridge
    canonical_repository_native_depth_bridge_witness

end Chronos.Frontier
