import Chronos.Frontier.FirstTargetNaturalAdmissibilityCertificateFrontier

namespace Chronos
namespace Frontier

/--
A named concrete target application for the first natural-admissibility
certificate.

This is deliberately minimal: it witnesses the certificate interface for one
concrete computable finite target only.
-/
def firstNamedConcreteTargetApplication :
    ComputableFiniteAdmissibleClass where
  objectCount := 1
  semanticRankRate := 0
  fiberEntropyGap := 1
  admissible := True
  finite_support := by decide
  semantic_rank_rate_computable := ⟨0, rfl⟩
  fiber_entropy_gap_computable := ⟨1, rfl⟩

theorem firstNamedConcreteTargetApplication_admissible :
    firstNamedConcreteTargetApplication.admissible := by
  trivial

theorem firstNamedConcreteTargetApplication_rank_entropy_dominance :
    SemanticRankRate firstNamedConcreteTargetApplication ≤
      FiberEntropyGap firstNamedConcreteTargetApplication := by
  decide

def firstNamedConcreteNaturalAdmissibilityCertificate :
    NaturalAdmissibilityDominanceCertificate
      firstNamedConcreteTargetApplication where
  admissible_witness :=
    firstNamedConcreteTargetApplication_admissible
  rank_entropy_dominance :=
    firstNamedConcreteTargetApplication_rank_entropy_dominance

def firstNamedConcreteCertificateFrontier :
    FirstTargetNaturalAdmissibilityCertificateFrontier
      firstNamedConcreteTargetApplication where
  certificate :=
    firstNamedConcreteNaturalAdmissibilityCertificate

theorem firstNamedConcreteTargetYieldsNaturalDominance :
    Nonempty NaturalDominanceAdmissibleComputableClass := by
  exact firstTargetNaturalAdmissibilityCertificateFrontier_to_natural
    firstNamedConcreteCertificateFrontier

end Frontier
end Chronos
