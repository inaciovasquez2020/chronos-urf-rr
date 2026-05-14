# FO4 Colap_R Open Problem Surface

Status: OPEN_PROBLEM_REQUIRED.

Closed surface:

```lean
def ColapR (G : GraphDatum) (R : Nat) : Type :=
  F2WeightedOverlapRelation G R
Problem surface:
def FO4CycleOverlapRankBoundProblem : Prop :=
  ∀ Δ R : Nat,
    ∃ C : Nat,
      ∀ X : FO4HomogeneousInput,
        X.Delta = Δ →
        X.R = R →
        FO4Homogeneous X →
        ColapRankBoundedAt X C
Next missing object:
finite FO4 radius-R type enumeration under degree bound Delta
Minimal missing lemma:
FO4-local indistinguishability under bounded degree implies uniformly bounded radius-R cycle-overlap rank.
Boundary:
Defines ColapR only.
Does not prove finite FO4 radius-R type enumeration.
Does not prove bounded cycle-overlap rank.
Does not close rigidity.
Does not prove P vs NP.
Does not solve any Clay problem.
