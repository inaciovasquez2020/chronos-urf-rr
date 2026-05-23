import Chronos.Frontier.GenuineAnalyticEstimatePackageProofReduction

namespace Chronos
namespace Frontier

/--
The four analytic PDE components required to instantiate
`GenuinePDEEstimateWitness`.

This structure records the theorem ingredients explicitly:
1. constraint propagation
2. energy-condition preservation
3. continuation up to collapse threshold
4. collapse criterion from restricted seed

Boundary: the file proves assembly from supplied components. It does not prove
the PDE estimates themselves.
-/
structure GenuinePDEEstimateWitnessComponents
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D)
    (G : GenuineEinsteinMatterDatum D) where
  h_nonSynthetic : G.nonSynthetic
  h_fourDimensionalPDEData : G.fourDimensionalPDEData
  h_genuineEinsteinMatterEquations : G.genuineEinsteinMatterEquations
  h_nonSymmetricRegime : G.nonSymmetricRegime
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

  collapse_criterion_from_restricted_seed :
    D.wellposedContinuation →
    R.boundary_accessible_observable →
    D.collapseCriterion

/--
Assembly theorem: the four supplied PDE components construct the
`GenuinePDEEstimateWitness`.
-/
def genuinePDEEstimateWitness_from_components
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (C : GenuinePDEEstimateWitnessComponents D R G) :
    GenuinePDEEstimateWitness D R :=
  {
    genuineDatum := G
    h_nonSynthetic := C.h_nonSynthetic
    h_fourDimensionalPDEData := C.h_fourDimensionalPDEData
    h_genuineEinsteinMatterEquations := C.h_genuineEinsteinMatterEquations
    h_nonSymmetricRegime := C.h_nonSymmetricRegime
    h_dimension := C.h_dimension
    h_nonsymmetric := C.h_nonsymmetric
    h_field := C.h_field
    h_physical := C.h_physical
    h_boundary := C.h_boundary
    h_finite_or_entropy := C.h_finite_or_entropy
    h_spectral := C.h_spectral
    h_finite_energy := C.h_finite_energy
    h_backreaction := C.h_backreaction
    constraint_propagation := C.constraint_propagation
    energy_condition_preservation := C.energy_condition_preservation
    continuation_up_to_collapse_threshold :=
      C.continuation_up_to_collapse_threshold
    collapse_criterion_from_seed :=
      C.collapse_criterion_from_restricted_seed
  }

/--
The four supplied PDE components imply analytic package existence.
-/
theorem analyticEstimatePackageExists_from_genuinePDEComponents
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (C : GenuinePDEEstimateWitnessComponents D R G) :
    AnalyticEstimatePackageExists :=
  analyticEstimatePackageExists_from_genuinePDEEstimateWitness
    (genuinePDEEstimateWitness_from_components C)

/--
The four supplied PDE components imply the bootstrap kernel.
-/
theorem bootstrapKernel_from_genuinePDEComponents
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (C : GenuinePDEEstimateWitnessComponents D R G) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      NonSymmetricEinsteinMatterBootstrapKernel D :=
  bootstrapKernel_from_genuinePDEEstimateWitness
    (genuinePDEEstimateWitness_from_components C)

/--
The four supplied PDE components imply the collapse-gate conclusion.
-/
theorem collapseGate_from_genuinePDEComponents
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (C : GenuinePDEEstimateWitnessComponents D R G) :
    ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
      D.collapseCriterion :=
  collapseGate_from_genuinePDEEstimateWitness
    (genuinePDEEstimateWitness_from_components C)

/--
Exact remaining theorem-level target.
-/
def GenuinePDEEstimateWitnessComponentsExist : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
  ∃ G : GenuineEinsteinMatterDatum D,
    Nonempty (GenuinePDEEstimateWitnessComponents D R G)

end Frontier
end Chronos
