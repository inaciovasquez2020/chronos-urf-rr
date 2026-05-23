import Chronos.Frontier.GravityClosureKernelTarget

namespace Chronos
namespace Frontier

/--
Toolkit-level admissible region for the gravity PDE route.

This is not an unrestricted gravity theorem. It records the restricted
physical/analytic envelope inside which an estimate package may be supplied.
-/
structure ToolkitAdmissibleRegion
    (D : FourDimensionalNonSymmetricEinsteinMatterData) where
  physically_admissible_region : Prop
  boundary_accessible_observable : Prop
  finite_detector_algebra_or_covariant_entropy_bound : Prop
  spectral_cutoff : Prop
  finite_energy_matter_admissible : Prop
  backreaction_controlled : Prop

/--
Analytic certificate package needed to supply the bootstrap kernel fields.
-/
structure AnalyticEstimatePackage
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D) where
  constraint_propagation :
    D.einsteinMatterSystem →
    D.einsteinMatterSystem

  energy_condition_preservation :
    R.finite_energy_matter_admissible →
    D.energyConditionPreserved

  continuation_up_to_collapse_threshold :
    D.einsteinMatterSystem →
    D.energyConditionPreserved →
    R.backreaction_controlled →
    D.wellposedContinuation

  collapse_criterion_from_seed :
    D.wellposedContinuation →
    R.boundary_accessible_observable →
    D.collapseCriterion

/--
Conditional analytic estimate package existence target.

This is a proposition, not a declared theorem constant.
-/
def AnalyticEstimatePackageExists : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
    D.spacetimeDimension = 4 ∧
    D.nonSymmetricMetric ∧
    D.einsteinMatterSystem ∧
    R.physically_admissible_region ∧
    R.boundary_accessible_observable ∧
    R.finite_detector_algebra_or_covariant_entropy_bound ∧
    R.spectral_cutoff ∧
    R.finite_energy_matter_admissible ∧
    R.backreaction_controlled ∧
    Nonempty (AnalyticEstimatePackage D R)

/--
The analytic existence target supplies a bootstrap kernel after unpacking its
certificate package.
-/
theorem bootstrapKernel_from_analyticEstimatePackageExists
    (h : AnalyticEstimatePackageExists) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      NonSymmetricEinsteinMatterBootstrapKernel D := by
  rcases h with
    ⟨D, R, h4, hnon, hfield, _hphys, hboundary, _hfiniteOrEntropy,
      _hspectral, hfiniteEnergy, hbackreaction, hpkg⟩
  rcases hpkg with ⟨A⟩
  let henergy : D.energyConditionPreserved :=
    A.energy_condition_preservation hfiniteEnergy
  let hcont : D.wellposedContinuation :=
    A.continuation_up_to_collapse_threshold
      hfield
      henergy
      hbackreaction
  let hgate : D.collapseCriterion :=
    A.collapse_criterion_from_seed
      hcont
      hboundary
  exact ⟨D,
    {
      dimension_four := h4
      nonsymmetric := hnon
      field_system := hfield
      energy_condition := henergy
      continuation := hcont
      collapse_gate := hgate
    }⟩

/--
The collapse-gate conclusion follows conditionally from the supplied analytic
package existence proposition.
-/
theorem collapseGate_from_analyticEstimatePackageExists
    (h : AnalyticEstimatePackageExists) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      D.collapseCriterion := by
  rcases bootstrapKernel_from_analyticEstimatePackageExists h with ⟨D, K⟩
  exact ⟨D, collapseGate_from_bootstrapKernel K⟩

end Frontier
end Chronos
