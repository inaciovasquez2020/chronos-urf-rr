import Chronos.Frontier.FO4SemanticCompletenessToColapRankControl

namespace Chronos.Frontier

structure FO4ColapCycleOverlapInput where
  Delta : Nat
  R : Nat

def FO4ColapCycleOverlapHomogeneous (_X : FO4ColapCycleOverlapInput) : Prop :=
  True

def FO4ColapRankBoundedAt (_X : FO4ColapCycleOverlapInput) (_C : Nat) : Prop :=
  True

def CycleOverlapRankBoundedAt (_X : FO4ColapCycleOverlapInput) (_B : Nat) : Prop :=
  True

def ColapRankControlImpliesBoundedCycleOverlapRank (Delta R : Nat) : Prop :=
  (∃ C : Nat,
    ∀ X : FO4ColapCycleOverlapInput,
      X.Delta = Delta →
      X.R = R →
      FO4ColapCycleOverlapHomogeneous X →
      FO4ColapRankBoundedAt X C) →
  ∃ B : Nat,
    ∀ X : FO4ColapCycleOverlapInput,
      X.Delta = Delta →
      X.R = R →
      FO4ColapCycleOverlapHomogeneous X →
      CycleOverlapRankBoundedAt X B

def PointwiseColapRankBoundsCycleOverlapRank : Prop :=
  ∃ f : Nat → Nat,
    ∀ X : FO4ColapCycleOverlapInput,
      ∀ C : Nat,
        FO4ColapRankBoundedAt X C →
        CycleOverlapRankBoundedAt X (f C)

theorem colap_rank_control_implies_bounded_cycle_overlap_rank
    (Delta R : Nat)
    (hpoint : PointwiseColapRankBoundsCycleOverlapRank) :
    ColapRankControlImpliesBoundedCycleOverlapRank Delta R := by
  intro hcolap
  rcases hpoint with ⟨f, hf⟩
  rcases hcolap with ⟨C, hC⟩
  exact ⟨f C, by
    intro X hDelta hR hhom
    exact hf X C (hC X hDelta hR hhom)⟩

end Chronos.Frontier
