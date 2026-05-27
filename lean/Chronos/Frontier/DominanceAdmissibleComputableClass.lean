import Chronos.Frontier.RawAdmissibilityObstructionForComputableClass

namespace Chronos
namespace Frontier

structure DominanceAdmissibleComputableClass where
  base : ComputableFiniteAdmissibleClass
  admissible_witness : base.admissible
  rank_entropy_dominance :
    SemanticRankRate base ≤ FiberEntropyGap base

def DominanceSemanticRankRate
    (X : DominanceAdmissibleComputableClass) : Nat :=
  SemanticRankRate X.base

def DominanceFiberEntropyGap
    (X : DominanceAdmissibleComputableClass) : Nat :=
  FiberEntropyGap X.base

theorem dominance_admissible_bridge
    (X : DominanceAdmissibleComputableClass) :
    DominanceSemanticRankRate X ≤ DominanceFiberEntropyGap X := by
  exact X.rank_entropy_dominance

theorem dominance_admissible_finite_support
    (X : DominanceAdmissibleComputableClass) :
    X.base.objectCount > 0 := by
  exact X.base.finite_support

theorem dominance_admissible_semantic_rank_computable
    (X : DominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = DominanceSemanticRankRate X := by
  exact X.base.semantic_rank_rate_computable

theorem dominance_admissible_fiber_entropy_computable
    (X : DominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = DominanceFiberEntropyGap X := by
  exact X.base.fiber_entropy_gap_computable

def DominanceAdmissibleToStructured
    (X : DominanceAdmissibleComputableClass) :
    StructuredAdmissibilityDominance X.base where
  admissible_witness := X.admissible_witness
  rank_entropy_dominance := X.rank_entropy_dominance

theorem dominance_admissible_supplies_structured_bridge
    (X : DominanceAdmissibleComputableClass) :
    SemanticRankRate X.base ≤ FiberEntropyGap X.base := by
  exact (DominanceAdmissibleToStructured X).rank_entropy_dominance

def DominanceAdmissibleReplacementLaw : Prop :=
  ∀ X : DominanceAdmissibleComputableClass,
    DominanceSemanticRankRate X ≤ DominanceFiberEntropyGap X

theorem dominance_admissible_replacement_law :
    DominanceAdmissibleReplacementLaw := by
  intro X
  exact dominance_admissible_bridge X

end Frontier
end Chronos
