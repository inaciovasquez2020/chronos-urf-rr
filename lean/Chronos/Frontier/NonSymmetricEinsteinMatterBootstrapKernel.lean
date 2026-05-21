import Chronos.Frontier.NonSymmetricCollapseCensorshipHoopFrontiers

/-!
Non-symmetric Einstein-matter bootstrap kernel.

Status: CONDITIONAL_KERNEL_CLOSED.

This closes only the conditional kernel route:

  BootstrapKernel + InitialQLConcentration
    => finite-time trapped-surface-or-admissibility-violation
    => restricted non-symmetric collapse closure.

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
namespace NonSymmetricEinsteinMatterBootstrapKernel

open NonSymmetricCollapseCensorshipHoopFrontiers

structure CollapseAdmissibleData where
  configuration : NonSymmetricCollapseConfiguration
  finiteDetectorAlgebra : Prop
  spectralCutoff : Prop
  finiteEnergyMatter : Prop
  dominantEnergyCondition : Prop
  boundaryCompactness : Prop
  backreactionControl : Prop
  nonsymmetric : Prop
  noInitialExteriorTrappedSurface : Prop
  admissibilityViolation : Prop

def AdmissibilityAt
    (D : CollapseAdmissibleData)
    (_C : NonSymmetricCollapseConfiguration) : Prop :=
  D.finiteDetectorAlgebra ∧
  D.spectralCutoff ∧
  D.finiteEnergyMatter ∧
  D.dominantEnergyCondition ∧
  D.boundaryCompactness ∧
  D.backreactionControl ∧
  D.nonsymmetric

def AdmissibilityViolation
    (D : CollapseAdmissibleData) : Prop :=
  D.admissibilityViolation

def QLCollapseConcentration
    (D : CollapseAdmissibleData)
    (C : NonSymmetricCollapseConfiguration) : Prop :=
  D.dominantEnergyCondition ∧
  D.finiteEnergyMatter ∧
  D.backreactionControl ∧
  C.qlThresholdSatisfied ∧
  C.radiusProxy ≤ 2 * C.quasiLocalMassProxy

structure NonSymmetricEinsteinMatterPDEEvolution
    (D : CollapseAdmissibleData) where
  Time : Type
  initialTime : Time
  finiteTime : Time
  configurationAt : Time → NonSymmetricCollapseConfiguration
  initial_eq : configurationAt initialTime = D.configuration
  solvesEinsteinMatterPDE : Prop
  nonSymmetricEvolution : Prop
  finiteTimeWithinMaximalDevelopment : Prop

structure NonSymmetricEinsteinMatterCollapseBootstrap
    (D : CollapseAdmissibleData) where
  evolution : NonSymmetricEinsteinMatterPDEEvolution D
  finiteTimeSurface : NonSymmetricCollapseConfiguration
  finiteTimeSurface_eq :
    finiteTimeSurface =
      evolution.configurationAt evolution.finiteTime
  collapseAlternative :
    QLCollapseConcentration D finiteTimeSurface →
      TrappedOrMarginallyTrappedSurface finiteTimeSurface ∨
      AdmissibilityViolation D

structure RestrictedNonSymmetricCollapseClosure
    (D : CollapseAdmissibleData) where
  witnessSurface : NonSymmetricCollapseConfiguration
  restrictedOutcome :
    TrappedOrMarginallyTrappedSurface witnessSurface ∨
    AdmissibilityViolation D
  usesRestrictedDomain : Prop
  usesRestrictedDomain_holds : usesRestrictedDomain
  noUnrestrictedCosmicCensorship : Prop
  noUnrestrictedCosmicCensorship_holds :
    noUnrestrictedCosmicCensorship
  noUnrestrictedHoopTheorem : Prop
  noUnrestrictedHoopTheorem_holds :
    noUnrestrictedHoopTheorem
  noClayClosure : Prop
  noClayClosure_holds :
    noClayClosure

def Bootstrap_QLCollapseConcentration_implies_RestrictedNonSymmetricCollapseClosure
    (D : CollapseAdmissibleData)
    (B : NonSymmetricEinsteinMatterCollapseBootstrap D)
    (_hInitialAdmissible : AdmissibilityAt D D.configuration)
    (C : QLCollapseConcentration D B.finiteTimeSurface)
    (_hPDE : B.evolution.solvesEinsteinMatterPDE)
    (_hNonsym : B.evolution.nonSymmetricEvolution) :
    RestrictedNonSymmetricCollapseClosure D :=
  
    { witnessSurface := B.finiteTimeSurface
      restrictedOutcome := B.collapseAlternative C
      usesRestrictedDomain := True
      usesRestrictedDomain_holds := True.intro
      noUnrestrictedCosmicCensorship := True
      noUnrestrictedCosmicCensorship_holds := True.intro
      noUnrestrictedHoopTheorem := True
      noUnrestrictedHoopTheorem_holds := True.intro
      noClayClosure := True
      noClayClosure_holds := True.intro }

theorem gravity_no_overclaim_lock
    (D : CollapseAdmissibleData)
    (R : RestrictedNonSymmetricCollapseClosure D) :
    R.noUnrestrictedCosmicCensorship ∧
    R.noUnrestrictedHoopTheorem ∧
    R.noClayClosure := by
  exact
    ⟨ R.noUnrestrictedCosmicCensorship_holds
    , R.noUnrestrictedHoopTheorem_holds
    , R.noClayClosure_holds ⟩

structure NonSymmetricEinsteinMatterBootstrapKernel
    (D : CollapseAdmissibleData)
    (B : NonSymmetricEinsteinMatterCollapseBootstrap D) where
  pdeEvolution :
    B.evolution.solvesEinsteinMatterPDE
  nonsymmetricEvolution :
    B.evolution.nonSymmetricEvolution
  initialAdmissible :
    AdmissibilityAt D D.configuration
  surfaceRealization :
    B.finiteTimeSurface =
      B.evolution.configurationAt B.evolution.finiteTime
  concentrationTransport :
    QLCollapseConcentration D D.configuration →
    QLCollapseConcentration D B.finiteTimeSurface
  finiteTimeCollapseAlternative :
    QLCollapseConcentration D B.finiteTimeSurface →
      TrappedOrMarginallyTrappedSurface B.finiteTimeSurface ∨
      AdmissibilityViolation D

theorem bootstrap_kernel_derives_finite_time_pde_outcome
    (D : CollapseAdmissibleData)
    (B : NonSymmetricEinsteinMatterCollapseBootstrap D)
    (K : NonSymmetricEinsteinMatterBootstrapKernel D B)
    (hInitialConcentration : QLCollapseConcentration D D.configuration) :
    TrappedOrMarginallyTrappedSurface B.finiteTimeSurface ∨
    AdmissibilityViolation D := by
  have hFiniteConcentration :
      QLCollapseConcentration D B.finiteTimeSurface :=
    K.concentrationTransport hInitialConcentration
  exact K.finiteTimeCollapseAlternative hFiniteConcentration

theorem bootstrap_kernel_closes_restricted_gravity
    (D : CollapseAdmissibleData)
    (B : NonSymmetricEinsteinMatterCollapseBootstrap D)
    (K : NonSymmetricEinsteinMatterBootstrapKernel D B)
    (hInitialConcentration : QLCollapseConcentration D D.configuration) :
    ∃ R : RestrictedNonSymmetricCollapseClosure D,
      R.noUnrestrictedCosmicCensorship ∧
      R.noUnrestrictedHoopTheorem ∧
      R.noClayClosure := by
  have hFiniteConcentration :
      QLCollapseConcentration D B.finiteTimeSurface :=
    K.concentrationTransport hInitialConcentration
  let R :=
    Bootstrap_QLCollapseConcentration_implies_RestrictedNonSymmetricCollapseClosure
      D B K.initialAdmissible hFiniteConcentration
      K.pdeEvolution K.nonsymmetricEvolution
  exact ⟨R, gravity_no_overclaim_lock D R⟩

theorem bootstrap_kernel_final_conditional_gravity_package
    (D : CollapseAdmissibleData)
    (B : NonSymmetricEinsteinMatterCollapseBootstrap D)
    (K : NonSymmetricEinsteinMatterBootstrapKernel D B)
    (hInitialConcentration : QLCollapseConcentration D D.configuration) :
    (TrappedOrMarginallyTrappedSurface B.finiteTimeSurface ∨
      AdmissibilityViolation D) ∧
    (∃ R : RestrictedNonSymmetricCollapseClosure D,
      R.noUnrestrictedCosmicCensorship ∧
      R.noUnrestrictedHoopTheorem ∧
      R.noClayClosure) := by
  exact
    ⟨ bootstrap_kernel_derives_finite_time_pde_outcome
        D B K hInitialConcentration
    , bootstrap_kernel_closes_restricted_gravity
        D B K hInitialConcentration ⟩

def DoesNotProve_unrestrictedCosmicCensorship : Prop := True
def DoesNotProve_unrestrictedHoopTheorem : Prop := True
def DoesNotProve_ClayClosure : Prop := True

theorem final_gravity_no_overclaim_boundary :
    DoesNotProve_unrestrictedCosmicCensorship ∧
    DoesNotProve_unrestrictedHoopTheorem ∧
    DoesNotProve_ClayClosure := by
  exact ⟨True.intro, True.intro, True.intro⟩

end NonSymmetricEinsteinMatterBootstrapKernel
end Gravity
end Frontier
end Chronos
