import Chronos.Frontier.LatentTraceEntropyRoute

namespace Chronos

def CarrierRankSoundness (sys : DynamicalSystem) : Prop :=
  ∀ ρ : Set (Set sys.State),
    (∃ n : Nat, sys.rankRate ρ n > 0) →
    NonNullFiberWitness sys

theorem restrictedRankRateBridge
    (lam : ℝ)
    (sys : DynamicalSystem)
    (h_sound : CarrierRankSoundness sys)
    (_h_rate : RateThickClass lam sys)
    (ρ : Set (Set sys.State))
    (hρ : ∃ n : Nat, sys.rankRate ρ n > 0) :
    NonNullFiberWitness sys := by
  exact h_sound ρ hρ

theorem restrictedRankRateBridge_fromLowerBound
    (lam : ℝ)
    (h_lam : lam > 0)
    (sys : DynamicalSystem)
    (h_sound : CarrierRankSoundness sys)
    (_h_rate : RateThickClass lam sys)
    (ρ : Set (Set sys.State))
    (hρ : ∃ n : Nat, sys.rankRate ρ n ≥ lam) :
    NonNullFiberWitness sys := by
  rcases hρ with ⟨n, hn⟩
  exact h_sound ρ ⟨n, lt_of_lt_of_le h_lam hn⟩

end Chronos
