namespace Chronos.Frontier.FO4CycleOverlapOpenProblemRequired

structure FO4GraphSemanticRankInput where
  Delta : Nat
  R : Nat
  colapRank : Nat
  cycleOverlapRank : Nat

def GraphSemanticCycleOverlapRankDominatedByColapRank : Prop :=
  ∀ X : FO4GraphSemanticRankInput,
    X.cycleOverlapRank ≤ X.colapRank

def counterexample : FO4GraphSemanticRankInput :=
  { Delta := 0, R := 0, colapRank := 0, cycleOverlapRank := 1 }

theorem unrestricted_graph_semantic_cycle_overlap_dominated_false :
    ¬ GraphSemanticCycleOverlapRankDominatedByColapRank := by
  intro h
  exact Nat.not_succ_le_zero 0 (h counterexample)

structure FO4GraphSemanticRankInputRestricted where
  Delta : Nat
  R : Nat
  colapRank : Nat
  cycleOverlapRank : Nat
  cycleOverlap_le_colap : cycleOverlapRank ≤ colapRank

def GraphSemanticCycleOverlapRankDominatedByColapRankRestricted : Prop :=
  ∀ X : FO4GraphSemanticRankInputRestricted,
    X.cycleOverlapRank ≤ X.colapRank

theorem restricted_graph_semantic_cycle_overlap_dominated_closed :
    GraphSemanticCycleOverlapRankDominatedByColapRankRestricted := by
  intro X
  exact X.cycleOverlap_le_colap

inductive FO4CycleOverlapRankStatus where
  | open_problem_required

def theoremLevelStatus : FO4CycleOverlapRankStatus :=
  FO4CycleOverlapRankStatus.open_problem_required

end Chronos.Frontier.FO4CycleOverlapOpenProblemRequired
