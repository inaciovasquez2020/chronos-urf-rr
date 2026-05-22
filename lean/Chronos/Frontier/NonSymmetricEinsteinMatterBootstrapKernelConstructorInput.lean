import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelExistenceFrontier

/-!
Non-symmetric Einstein-matter bootstrap kernel constructor input.

Status: CONSTRUCTOR_INPUT_ONLY_TARGET_REDUCED_NOT_SOLVED.

This file reduces the current gravity blocker to the exact constructor fields
needed to build `NonSymmetricEinsteinMatterBootstrapKernel`.

Boundary:
This does not prove unrestricted cosmic censorship.
This does not prove the unrestricted hoop theorem.
This does not prove unrestricted QL_CollapseGate.
This does not prove unrestricted UniversalBoundaryCompactness.
This does not prove P vs NP.
This does not prove any Clay problem.
-/

namespace Chronos
namespace Frontier
namespace Gravity
namespace NonSymmetricEinsteinMatterBootstrapKernelConstructorInput

open NonSymmetricCollapseCensorshipHoopFrontiers
open NonSymmetricEinsteinMatterBootstrapKernel
open NonSymmetricEinsteinMatterBootstrapKernelExistenceFrontier

structure NonSymmetricEinsteinMatterBootstrapKernelConstructorInput
    (G : GenuineNonSymmetricEinsteinMatterPDEData) where
  pdeEvolution : G.B.evolution.solvesEinsteinMatterPDE
  nonsymmetricEvolution : G.B.evolution.nonSymmetricEvolution
  initialAdmissible : AdmissibilityAt G.D G.D.configuration
  surfaceRealization :
    G.B.finiteTimeSurface =
      G.B.evolution.configurationAt G.B.evolution.finiteTime
  concentrationTransport :
    QLCollapseConcentration G.D G.D.configuration →
      QLCollapseConcentration G.D G.B.finiteTimeSurface
  finiteTimeCollapseAlternative :
    QLCollapseConcentration G.D G.B.finiteTimeSurface →
      TrappedOrMarginallyTrappedSurface G.B.finiteTimeSurface ∨
        AdmissibilityViolation G.D

def kernel_from_constructor_input
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelConstructorInput G) :
    NonSymmetricEinsteinMatterBootstrapKernel G.D G.B :=
  { pdeEvolution := H.pdeEvolution
    nonsymmetricEvolution := H.nonsymmetricEvolution
    initialAdmissible := H.initialAdmissible
    surfaceRealization := H.surfaceRealization
    concentrationTransport := H.concentrationTransport
    finiteTimeCollapseAlternative := H.finiteTimeCollapseAlternative }

theorem constructor_input_implies_existence_target
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelConstructorInput G) :
    NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget G := by
  exact ⟨kernel_from_constructor_input G H, True.intro⟩

theorem constructor_input_closes_conditional_gravity_package
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelConstructorInput G) :
    ∃ _K : NonSymmetricEinsteinMatterBootstrapKernel G.D G.B,
      (TrappedOrMarginallyTrappedSurface G.B.finiteTimeSurface ∨
        AdmissibilityViolation G.D) ∧
      (∃ R : RestrictedNonSymmetricCollapseClosure G.D,
        R.noUnrestrictedCosmicCensorship ∧
        R.noUnrestrictedHoopTheorem ∧
        R.noClayClosure) := by
  exact existence_target_closes_conditional_gravity_package G
    (constructor_input_implies_existence_target G H)

def DoesNotProve_unrestrictedCosmicCensorship : Prop := True
def DoesNotProve_unrestrictedHoopTheorem : Prop := True
def DoesNotProve_unrestrictedQLCollapseGate : Prop := True
def DoesNotProve_unrestrictedUniversalBoundaryCompactness : Prop := True
def DoesNotProve_PvsNP : Prop := True
def DoesNotProve_ClayClosure : Prop := True

theorem constructor_input_no_overclaim_boundary :
    DoesNotProve_unrestrictedCosmicCensorship ∧
    DoesNotProve_unrestrictedHoopTheorem ∧
    DoesNotProve_unrestrictedQLCollapseGate ∧
    DoesNotProve_unrestrictedUniversalBoundaryCompactness ∧
    DoesNotProve_PvsNP ∧
    DoesNotProve_ClayClosure := by
  exact ⟨True.intro, True.intro, True.intro, True.intro, True.intro, True.intro⟩

end NonSymmetricEinsteinMatterBootstrapKernelConstructorInput
end Gravity
end Frontier
end Chronos
