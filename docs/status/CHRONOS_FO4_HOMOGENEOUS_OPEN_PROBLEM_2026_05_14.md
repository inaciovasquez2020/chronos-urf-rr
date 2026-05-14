# FO4 Homogeneous Open Problem Surface

Status: OPEN_PROBLEM_REQUIRED.

Closed surface:

```lean
def FO4Homogeneous (X : FO4HomogeneousInput) : Prop :=
  X.degree_bounded ∧ X.radius_R_FO4_indistinguishable
Next missing object:
Colap_R(G) over F2.
Minimal missing lemma:
FO4-local indistinguishability under bounded degree implies uniformly bounded radius-R cycle-overlap rank.
Boundary:
Defines FO4Homogeneous only.
Does not define Colap_R.
Does not prove finite FO4 radius-R type enumeration.
Does not prove bounded cycle-overlap rank.
Does not close rigidity.
