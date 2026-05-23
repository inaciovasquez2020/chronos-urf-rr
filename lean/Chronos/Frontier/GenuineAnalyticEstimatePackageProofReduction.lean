import Chronos.Frontier.AnalyticEstimatePackageExistsProof

namespace Chronos
namespace Frontier

/--
Marker that the datum is not the synthetic interface witness.

This is intentionally a Prop field: the file proves a reduction from genuine
PDE certificates to the analytic package, not the PDE estimates themselves.
-/
structure GenuineEinsteinMatterDatum
    (D : FourDimensionalNonSymmetricEinsteinMatterData) where
  nonSynthetic : Prop
  fourDimensionalPDEData : Prop
  genuineEinsteinMatterEquations : Prop
  nonSymmetricRegime : Prop

/--
Genuine PDE certificate supply.

These are exactly the analytic ingredients still required from PDE analysis.
-/
structure GenuinePDEEstimateWitness
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D) where
  genuineDatum : GenuineEinsteinMatterDatum D
  h_nonSynthetic : genuineDatum.nonSynthetic
  h_fourDimensionalPDEData : genuineDatum.fourDimensionalPDEData
  h_genuineEinsteinMatterEquations : genuineDatum.genuineEinsteinMatterEquations
  h_nonSymmetricRegime : genuineDatum.nonSymmetricRegime
  h_dimension : D.spacetimeDimension = 4
  h_nonsymmetric : D.nonSymmetricMetric
  h_field : D.einsteinMatterSystem
  h_physical : R.physically_admissible_region
  h_boundary : R.boundary_accessible_observable
  h_finite_or_entropy : R.finite_detector_algebra_or_covariant_entropy_bound
  h_spectral : R.spectral_cutoff
  h_finite_energy : R.finite_energy_matter_admissible
  h_backreaction : R.backreaction_controlled
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
Build the abstract analytic package from genuine PDE estimates.
-/
def analyticEstimatePackage_from_genuinePDEEstimateWitness
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    (W : GenuinePDEEstimateWitness D R) :
    AnalyticEstimatePackage D R :=
  {
    constraint_propagation := W.constraint_propagation
    energy_condition_preservation := W.energy_condition_preservation
    continuation_up_to_collapse_threshold :=
      W.continuation_up_to_collapse_threshold
    collapse_criterion_from_seed := W.collapse_criterion_from_seed
  }

/--
A genuine PDE estimate witness proves analytic package existence.
-/
theorem analyticEstimatePackageExists_from_genuinePDEEstimateWitness
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    (W : GenuinePDEEstimateWitness D R) :
    AnalyticEstimatePackageExists := by
  exact ⟨
    D,
    R,
    W.h_dimension,
    W.h_nonsymmetric,
    W.h_field,
    W.h_physical,
    W.h_boundary,
    W.h_finite_or_entropy,
    W.h_spectral,
    W.h_finite_energy,
    W.h_backreaction,
    ⟨analyticEstimatePackage_from_genuinePDEEstimateWitness W⟩
  ⟩

/--
A genuine PDE estimate witness supplies a bootstrap kernel.
-/
theorem bootstrapKernel_from_genuinePDEEstimateWitness
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    (W : GenuinePDEEstimateWitness D R) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      NonSymmetricEinsteinMatterBootstrapKernel D :=
  bootstrapKernel_from_analyticEstimatePackageExists
    (analyticEstimatePackageExists_from_genuinePDEEstimateWitness W)

/--
A genuine PDE estimate witness supplies the collapse-gate conclusion.
-/
theorem collapseGate_from_genuinePDEEstimateWitness
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    (W : GenuinePDEEstimateWitness D R) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      D.collapseCriterion :=
  collapseGate_from_analyticEstimatePackageExists
    (analyticEstimatePackageExists_from_genuinePDEEstimateWitness W)

/--
The exact remaining theorem-level object.
-/
def GenuineAnalyticEstimatePackageExistsProof : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
    Nonempty (GenuinePDEEstimateWitness D R)

/--
If the genuine PDE witness exists, the analytic estimate package exists.
-/
theorem analyticEstimatePackageExists_from_genuineProof
    (h : GenuineAnalyticEstimatePackageExistsProof) :
    AnalyticEstimatePackageExists := by
  rcases h with ⟨D, R, hW⟩
  rcases hW with ⟨W⟩
  exact analyticEstimatePackageExists_from_genuinePDEEstimateWitness W

end Frontier
end Chronos
