import Chronos.Frontier.NonPropSemanticRankRateToFiberEntropySoundness

namespace Chronos.Frontier

/--
Repository-native universal fiber-entropy gap witness surface.

This is a numerical witness surface only: it records existence of a positive
rational fiber-entropy gap extracted from a non-Prop semantic rank-rate datum.
-/
def RepositoryNativeUniversalFiberEntropyGap : Prop :=
  ∃ ε : ℚ, 0 < ε

theorem repository_native_universal_fiber_entropy_gap_from_nonprop_soundness
    (D : NonPropSemanticRankRateDatum) :
    RepositoryNativeUniversalFiberEntropyGap := by
  rcases nonprop_semantic_rank_rate_to_fiber_entropy_soundness D with
    ⟨ε, hε_pos, _hε_le⟩
  exact ⟨ε, hε_pos⟩

theorem canonical_repository_native_universal_fiber_entropy_gap :
    RepositoryNativeUniversalFiberEntropyGap := by
  exact repository_native_universal_fiber_entropy_gap_from_nonprop_soundness
    canonicalNonPropSemanticRankRateDatum

end Chronos.Frontier
