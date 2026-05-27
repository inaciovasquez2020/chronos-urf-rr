import Chronos.Frontier.NamedConcreteNaturalAdmissibilityCertificate
import Chronos.Frontier.FiniteRegisteredHyperbolicRateThickAssembly

namespace Chronos
namespace Frontier

open FiniteRegisteredHyperbolicRateThickAssembly

noncomputable section

def finiteRegisteredHyperbolicConcreteSystem :
    UniformlyHyperbolicAdmissibleSystem where
  lam := (1 / 4 : ℝ)
  entropyMass := 1
  lam_admissible := by
    constructor <;> norm_num

def finiteRegisteredHyperbolicConcreteRegistry :
    FiniteHyperbolicRegistry 1 where
  system := fun _ => finiteRegisteredHyperbolicConcreteSystem

theorem finiteRegisteredHyperbolicConcreteFloor :
    ∀ i : Fin 1,
      (1 : ℝ) ≤
        (finiteRegisteredHyperbolicConcreteRegistry.system i).entropyMass := by
  intro i
  fin_cases i
  norm_num [finiteRegisteredHyperbolicConcreteRegistry,
    finiteRegisteredHyperbolicConcreteSystem]

theorem finiteRegisteredHyperbolicConcreteUniversalGap :
    RegisteredHyperbolicUniversalFiberEntropyGap
      finiteRegisteredHyperbolicConcreteRegistry := by
  exact FiniteRegisteredHyperbolicRateThickUniversalGapAssembly
    finiteRegisteredHyperbolicConcreteRegistry
    1
    (by norm_num)
    finiteRegisteredHyperbolicConcreteFloor

def finiteRegisteredHyperbolicComputableTargetApplication :
    ComputableFiniteAdmissibleClass where
  objectCount := 1
  semanticRankRate := 1
  fiberEntropyGap := 1
  admissible :=
    RegisteredHyperbolicUniversalFiberEntropyGap
      finiteRegisteredHyperbolicConcreteRegistry
  finite_support := by decide
  semantic_rank_rate_computable := ⟨1, rfl⟩
  fiber_entropy_gap_computable := ⟨1, rfl⟩

def finiteRegisteredHyperbolicNaturalAdmissibilityCertificate :
    NaturalAdmissibilityDominanceCertificate
      finiteRegisteredHyperbolicComputableTargetApplication where
  admissible_witness :=
    finiteRegisteredHyperbolicConcreteUniversalGap
  rank_entropy_dominance := by
    decide

def finiteRegisteredHyperbolicCertificateFrontier :
    FirstTargetNaturalAdmissibilityCertificateFrontier
      finiteRegisteredHyperbolicComputableTargetApplication where
  certificate :=
    finiteRegisteredHyperbolicNaturalAdmissibilityCertificate

theorem finiteRegisteredHyperbolicTargetYieldsNaturalDominance :
    Nonempty NaturalDominanceAdmissibleComputableClass := by
  exact firstTargetNaturalAdmissibilityCertificateFrontier_to_natural
    finiteRegisteredHyperbolicCertificateFrontier

end

end Frontier
end Chronos
