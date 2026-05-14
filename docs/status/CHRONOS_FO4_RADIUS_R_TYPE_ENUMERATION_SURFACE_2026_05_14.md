# FO4 Radius-R Type Enumeration Surface

Status: FINITE_TYPE_ENUMERATION_SURFACE_CLOSED.

Closed surface:

```lean
def FO4RadiusRTypeBound (Delta R : Nat) : Nat :=
  (Delta + 2) ^ (R + 1)

structure FO4RadiusRTypeCode (Delta R : Nat) where
  code : Nat
  code_lt_bound : code < FO4RadiusRTypeBound Delta R
Closed theorem:
theorem fo4FiniteTypeEnumerationSurfaceClosed :
    FO4FiniteTypeEnumerationSurfaceClosed
Next missing lemma:
Semantic completeness: every bounded-degree FO4 radius-R neighborhood realizes one of the finite type codes in a way sufficient to control ColapR.
Boundary:
Code-level finite FO4 radius-R type enumeration surface only.
Does not prove semantic completeness of FO4 types.
Does not prove bounded cycle-overlap rank.
Does not close rigidity.
Does not prove P vs NP.
Does not solve any Clay problem.
