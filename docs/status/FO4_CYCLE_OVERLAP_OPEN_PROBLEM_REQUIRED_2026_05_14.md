# FO4 Cycle-Overlap Rank Open Problem Required

Status: OPEN_PROBLEM_REQUIRED

## Closed restricted surface

`FO4GraphSemanticRankInputRestricted` includes:

```lean
cycleOverlap_le_colap : cycleOverlapRank ≤ colapRank
Therefore the restricted domination statement is closed by field projection.
Unrestricted obstruction
The unrestricted object is:
def GraphSemanticCycleOverlapRankDominatedByColapRank : Prop :=
  ∀ X : FO4GraphSemanticRankInput,
    X.cycleOverlapRank ≤ X.colapRank
It is false under the current unrestricted structure.
Counterexample:
{ Delta := 0, R := 0, colapRank := 0, cycleOverlapRank := 1 }
Missing theorem-level object
A nontrivial theorem-level closure requires a graph-theoretic proof that the intended semantic cycle-overlap rank is always a subrank of the intended Colap rank.
Boundary
No unconditional graph-theoretic cycle-overlap rank bound is proved.
No rigidity closure is proved.
No P vs NP closure is proved.
No Clay-problem closure is proved.
