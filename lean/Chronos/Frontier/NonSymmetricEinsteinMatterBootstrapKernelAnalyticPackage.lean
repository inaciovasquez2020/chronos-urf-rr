import Chronos.Frontier.NonSymmetricEinsteinMatterBootstrapKernelConstructorInput

/-!
Non-symmetric Einstein-matter bootstrap kernel analytic package.

Status: ANALYTIC_PACKAGE_INPUT_ONLY_NOT_PROVED.

This file records the weakest admissible bundled analytic assumption
sufficient to instantiate the constructor input.

Boundary:
This does not prove the analytic package.
This does not prove pdeEvolution from PDE well-posedness.
This does not prove nonsymmetric evolution persistence.
This does not prove admissibility preservation.
This does not prove concentration transport.
This does not prove the finite-time collapse alternative.
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
namespace NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage

open NonSymmetricCollapseCensorshipHoopFrontiers
open NonSymmetricEinsteinMatterBootstrapKernel
open NonSymmetricEinsteinMatterBootstrapKernelExistenceFrontier
open NonSymmetricEinsteinMatterBootstrapKernelConstructorInput

structure NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage
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

def analytic_package_to_constructor_input
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage G) :
    NonSymmetricEinsteinMatterBootstrapKernelConstructorInput G :=
  { pdeEvolution := H.pdeEvolution
    nonsymmetricEvolution := H.nonsymmetricEvolution
    initialAdmissible := H.initialAdmissible
    surfaceRealization := H.surfaceRealization
    concentrationTransport := H.concentrationTransport
    finiteTimeCollapseAlternative := H.finiteTimeCollapseAlternative }

theorem analytic_package_implies_constructor_input
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage G) :
    NonSymmetricEinsteinMatterBootstrapKernelConstructorInput G :=
  analytic_package_to_constructor_input G H

theorem analytic_package_implies_existence_target
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage G) :
    NonSymmetricEinsteinMatterBootstrapKernelExistenceTarget G := by
  exact constructor_input_implies_existence_target G
    (analytic_package_implies_constructor_input G H)

theorem analytic_package_closes_conditional_gravity_package
    (G : GenuineNonSymmetricEinsteinMatterPDEData)
    (H : NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage G) :
    ∃ _K : NonSymmetricEinsteinMatterBootstrapKernel G.D G.B,
      (TrappedOrMarginallyTrappedSurface G.B.finiteTimeSurface ∨
        AdmissibilityViolation G.D) ∧
      (∃ R : RestrictedNonSymmetricCollapseClosure G.D,
        R.noUnrestrictedCosmicCensorship ∧
        R.noUnrestrictedHoopTheorem ∧
        R.noClayClosure) := by
  exact constructor_input_closes_conditional_gravity_package G
    (analytic_package_implies_constructor_input G H)

def DoesNotProve_analyticPackage : Prop := True
def DoesNotProve_pdeWellPosedness : Prop := True
def DoesNotProve_nonsymmetricEvolutionPersistence : Prop := True
def DoesNotProve_admissibilityPreservation : Prop := True
def DoesNotProve_concentrationTransport : Prop := True
def DoesNotProve_finiteTimeCollapseAlternative : Prop := True
def DoesNotProve_unrestrictedCosmicCensorship : Prop := True
def DoesNotProve_unrestrictedHoopTheorem : Prop := True
def DoesNotProve_unrestrictedQLCollapseGate : Prop := True
def DoesNotProve_unrestrictedUniversalBoundaryCompactness : Prop := True
def DoesNotProve_PvsNP : Prop := True
def DoesNotProve_ClayClosure : Prop := True

theorem analytic_package_no_overclaim_boundary :
    DoesNotProve_analyticPackage ∧
    DoesNotProve_pdeWellPosedness ∧
    DoesNotProve_nonsymmetricEvolutionPersistence ∧
    DoesNotProve_admissibilityPreservation ∧
    DoesNotProve_concentrationTransport ∧
    DoesNotProve_finiteTimeCollapseAlternative ∧
    DoesNotProve_unrestrictedCosmicCensorship ∧
    DoesNotProve_unrestrictedHoopTheorem ∧
    DoesNotProve_unrestrictedQLCollapseGate ∧
    DoesNotProve_unrestrictedUniversalBoundaryCompactness ∧
    DoesNotProve_PvsNP ∧
    DoesNotProve_ClayClosure := by
  exact ⟨True.intro, True.intro, True.intro, True.intro, True.intro, True.intro,
    True.intro, True.intro, True.intro, True.intro, True.intro, True.intro⟩

end NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage
end Gravity
end Frontier
end Chronos
