import Chronos.Frontier.DominanceAdmissibleComputableClass

namespace Chronos
namespace Frontier

/--
A natural admissibility interface for target applications.

This packages the exact data a target application must supply in order to
enter the dominance-admissible computable class.
-/
structure NaturalAdmissibilityDominanceCertificate
    (X : ComputableFiniteAdmissibleClass) where
  admissible_witness : X.admissible
  rank_entropy_dominance :
    SemanticRankRate X ≤ FiberEntropyGap X

/--
A target-facing admissible computable object.

The field `natural_certificate` is the bridge from application-specific
admissibility to dominance admissibility.
-/
structure NaturalDominanceAdmissibleComputableClass where
  base : ComputableFiniteAdmissibleClass
  natural_certificate :
    NaturalAdmissibilityDominanceCertificate base

def NaturalDominanceSemanticRankRate
    (X : NaturalDominanceAdmissibleComputableClass) : Nat :=
  SemanticRankRate X.base

def NaturalDominanceFiberEntropyGap
    (X : NaturalDominanceAdmissibleComputableClass) : Nat :=
  FiberEntropyGap X.base

def natural_to_dominance_admissible
    (X : NaturalDominanceAdmissibleComputableClass) :
    DominanceAdmissibleComputableClass where
  base := X.base
  admissible_witness := X.natural_certificate.admissible_witness
  rank_entropy_dominance := X.natural_certificate.rank_entropy_dominance

theorem natural_admissibility_supplies_dominance_class
    (X : NaturalDominanceAdmissibleComputableClass) :
    DominanceSemanticRankRate (natural_to_dominance_admissible X)
      ≤ DominanceFiberEntropyGap (natural_to_dominance_admissible X) := by
  exact dominance_admissible_bridge (natural_to_dominance_admissible X)

theorem natural_admissibility_bridge
    (X : NaturalDominanceAdmissibleComputableClass) :
    NaturalDominanceSemanticRankRate X ≤
      NaturalDominanceFiberEntropyGap X := by
  exact X.natural_certificate.rank_entropy_dominance

theorem natural_admissibility_finite_support
    (X : NaturalDominanceAdmissibleComputableClass) :
    X.base.objectCount > 0 := by
  exact X.base.finite_support

theorem natural_admissibility_semantic_rank_computable
    (X : NaturalDominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = NaturalDominanceSemanticRankRate X := by
  exact X.base.semantic_rank_rate_computable

theorem natural_admissibility_fiber_entropy_computable
    (X : NaturalDominanceAdmissibleComputableClass) :
    ∃ n : Nat, n = NaturalDominanceFiberEntropyGap X := by
  exact X.base.fiber_entropy_gap_computable

/--
Remaining application-level problem: each target application must construct
`NaturalAdmissibilityDominanceCertificate` from its own admissibility axioms.
-/
def TargetApplicationCertificateProblem : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    X.admissible →
      NaturalAdmissibilityDominanceCertificate X

end Frontier
end Chronos
