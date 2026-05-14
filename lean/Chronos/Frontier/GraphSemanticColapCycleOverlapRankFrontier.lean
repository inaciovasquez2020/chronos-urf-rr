import Chronos.Frontier.FO4PointwiseColapToCycleOverlapRank

namespace Chronos.Frontier

structure FO4GraphSemanticRankInput where
  Delta : Nat
  R : Nat
  colapRank : Nat
  cycleOverlapRank : Nat

def GraphSemanticFO4ColapRankBoundedAt
    (X : FO4GraphSemanticRankInput)
    (C : Nat) : Prop :=
  X.colapRank ≤ C

def GraphSemanticCycleOverlapRankBoundedAt
    (X : FO4GraphSemanticRankInput)
    (B : Nat) : Prop :=
  X.cycleOverlapRank ≤ B

def GraphSemanticPointwiseColapRankBoundsCycleOverlapRank : Prop :=
  ∃ f : Nat → Nat,
    ∀ X : FO4GraphSemanticRankInput,
      ∀ C : Nat,
        GraphSemanticFO4ColapRankBoundedAt X C →
        GraphSemanticCycleOverlapRankBoundedAt X (f C)

def GraphSemanticCycleOverlapRankDominatedByColapRank : Prop :=
  ∀ X : FO4GraphSemanticRankInput,
    X.cycleOverlapRank ≤ X.colapRank

theorem graph_semantic_pointwise_colap_rank_bounds_cycle_overlap_rank
    (hdom : GraphSemanticCycleOverlapRankDominatedByColapRank) :
    GraphSemanticPointwiseColapRankBoundsCycleOverlapRank := by
  refine ⟨fun C => C, ?_⟩
  intro X C hC
  exact Nat.le_trans (hdom X) hC

def GraphSemanticColapRankControlImpliesBoundedCycleOverlapRank
    (Delta R : Nat) : Prop :=
  (∃ C : Nat,
    ∀ X : FO4GraphSemanticRankInput,
      X.Delta = Delta →
      X.R = R →
      GraphSemanticFO4ColapRankBoundedAt X C) →
  ∃ B : Nat,
    ∀ X : FO4GraphSemanticRankInput,
      X.Delta = Delta →
      X.R = R →
      GraphSemanticCycleOverlapRankBoundedAt X B

theorem graph_semantic_colap_rank_control_implies_bounded_cycle_overlap_rank
    (Delta R : Nat)
    (hpoint : GraphSemanticPointwiseColapRankBoundsCycleOverlapRank) :
    GraphSemanticColapRankControlImpliesBoundedCycleOverlapRank Delta R := by
  intro hcolap
  rcases hpoint with ⟨f, hf⟩
  rcases hcolap with ⟨C, hC⟩
  exact ⟨f C, by
    intro X hDelta hR
    exact hf X C (hC X hDelta hR)⟩

theorem graph_semantic_colap_rank_control_implies_bounded_cycle_overlap_rank_from_domination
    (Delta R : Nat)
    (hdom : GraphSemanticCycleOverlapRankDominatedByColapRank) :
    GraphSemanticColapRankControlImpliesBoundedCycleOverlapRank Delta R :=
  graph_semantic_colap_rank_control_implies_bounded_cycle_overlap_rank
    Delta
    R
    (graph_semantic_pointwise_colap_rank_bounds_cycle_overlap_rank hdom)

end Chronos.Frontier
