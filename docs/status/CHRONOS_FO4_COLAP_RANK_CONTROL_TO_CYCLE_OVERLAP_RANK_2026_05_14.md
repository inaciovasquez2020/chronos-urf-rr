# FO4 Colap Rank Control to Cycle Overlap Rank

Status: CONDITIONAL_CYCLE_OVERLAP_RANK_INTERFACE_CLOSED.

Closed conditional interface:

```lean
def PointwiseColapRankBoundsCycleOverlapRank : Prop :=
  ∃ f : Nat → Nat,
    ∀ X : FO4HomogeneousInput,
      ∀ C : Nat,
        ColapRankBoundedAt X C →
        CycleOverlapRankBoundedAt X (f C)
Derived theorem:
theorem colap_rank_control_implies_bounded_cycle_overlap_rank
    (Delta R : Nat)
    (hpoint : PointwiseColapRankBoundsCycleOverlapRank) :
    ColapRankControlImpliesBoundedCycleOverlapRank Delta R
Boundary:
Does not prove PointwiseColapRankBoundsCycleOverlapRank.
Does not prove an unconditional cycle-overlap-rank bound.
Does not prove bounded cycle-overlap rank from graph semantics.
Does not prove rigidity closure.
Does not prove P vs NP.
Does not solve any Clay problem.
