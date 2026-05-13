import Chronos.Frontier.UniversalFiberEntropyGapFromNonPropSoundness

namespace Chronos.Frontier

/--
Repository-native depth lower-bound witness surface.

This is a numerical repository-native witness surface only. It converts a
positive rational fiber-entropy gap into the existence of a positive rational
depth lower-bound witness.
-/
def RepositoryNativeDepthBridgeWitness : Prop :=
  ∃ δ : ℚ, 0 < δ

theorem repository_native_depth_bridge_from_universal_fiber_entropy_gap
    (h : RepositoryNativeUniversalFiberEntropyGap) :
    RepositoryNativeDepthBridgeWitness := by
  rcases h with ⟨ε, hε_pos⟩
  exact ⟨ε, hε_pos⟩

theorem canonical_repository_native_depth_bridge_witness :
    RepositoryNativeDepthBridgeWitness := by
  exact repository_native_depth_bridge_from_universal_fiber_entropy_gap
    canonical_repository_native_universal_fiber_entropy_gap

end Chronos.Frontier
