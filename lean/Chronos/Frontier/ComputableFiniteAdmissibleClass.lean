namespace Chronos
namespace Frontier

/--
A finite admissible object whose two target quantities are explicitly computable
as natural-number data.

This is a concrete admissible class only. It does not assert any comparison,
positivity, approximation theorem, stability theorem, unrestricted lift, or
Chronos-RR consequence.
-/
structure ComputableFiniteAdmissibleClass where
  objectCount : Nat
  semanticRankRate : Nat
  fiberEntropyGap : Nat
  admissible : Prop
  finite_support : objectCount > 0
  semantic_rank_rate_computable : ∃ n : Nat, n = semanticRankRate
  fiber_entropy_gap_computable : ∃ n : Nat, n = fiberEntropyGap

def SemanticRankRate (X : ComputableFiniteAdmissibleClass) : Nat :=
  X.semanticRankRate

def FiberEntropyGap (X : ComputableFiniteAdmissibleClass) : Nat :=
  X.fiberEntropyGap

theorem semantic_rank_rate_is_computable
    (X : ComputableFiniteAdmissibleClass) :
    ∃ n : Nat, n = SemanticRankRate X := by
  exact X.semantic_rank_rate_computable

theorem fiber_entropy_gap_is_computable
    (X : ComputableFiniteAdmissibleClass) :
    ∃ n : Nat, n = FiberEntropyGap X := by
  exact X.fiber_entropy_gap_computable

theorem finite_support_positive
    (X : ComputableFiniteAdmissibleClass) :
    X.objectCount > 0 := by
  exact X.finite_support

end Frontier
end Chronos
