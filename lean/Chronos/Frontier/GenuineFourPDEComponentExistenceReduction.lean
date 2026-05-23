import Chronos.Frontier.GenuinePDEEstimateWitnessComponents

namespace Chronos
namespace Frontier

structure GenuineConstraintPropagationComponent
    (D : FourDimensionalNonSymmetricEinsteinMatterData) where
  constraint_propagation :
    D.einsteinMatterSystem →
    D.einsteinMatterSystem

structure GenuineEnergyConditionPreservationComponent
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D) where
  energy_condition_preservation :
    R.finite_energy_matter_admissible →
    D.energyConditionPreserved

structure GenuineContinuationUpToCollapseThresholdComponent
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D) where
  continuation_up_to_collapse_threshold :
    D.einsteinMatterSystem →
    D.energyConditionPreserved →
    R.backreaction_controlled →
    D.wellposedContinuation

structure GenuineCollapseCriterionFromRestrictedSeedComponent
    (D : FourDimensionalNonSymmetricEinsteinMatterData)
    (R : ToolkitAdmissibleRegion D) where
  collapse_criterion_from_restricted_seed :
    D.wellposedContinuation →
    R.boundary_accessible_observable →
    D.collapseCriterion

structure GenuineFourPDEComponentBase
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

def genuinePDEEstimateWitnessComponents_from_four_components
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (B : GenuineFourPDEComponentBase D R G)
    (C : GenuineConstraintPropagationComponent D)
    (E : GenuineEnergyConditionPreservationComponent D R)
    (T : GenuineContinuationUpToCollapseThresholdComponent D R)
    (K : GenuineCollapseCriterionFromRestrictedSeedComponent D R) :
    GenuinePDEEstimateWitnessComponents D R G :=
  {
    h_nonSynthetic := B.h_nonSynthetic
    h_fourDimensionalPDEData := B.h_fourDimensionalPDEData
    h_genuineEinsteinMatterEquations := B.h_genuineEinsteinMatterEquations
    h_nonSymmetricRegime := B.h_nonSymmetricRegime
    h_dimension := B.h_dimension
    h_nonsymmetric := B.h_nonsymmetric
    h_field := B.h_field
    h_physical := B.h_physical
    h_boundary := B.h_boundary
    h_finite_or_entropy := B.h_finite_or_entropy
    h_spectral := B.h_spectral
    h_finite_energy := B.h_finite_energy
    h_backreaction := B.h_backreaction
    constraint_propagation := C.constraint_propagation
    energy_condition_preservation := E.energy_condition_preservation
    continuation_up_to_collapse_threshold :=
      T.continuation_up_to_collapse_threshold
    collapse_criterion_from_restricted_seed :=
      K.collapse_criterion_from_restricted_seed
  }

theorem genuinePDEEstimateWitnessComponentsExist_from_four_components
    {D : FourDimensionalNonSymmetricEinsteinMatterData}
    {R : ToolkitAdmissibleRegion D}
    {G : GenuineEinsteinMatterDatum D}
    (B : GenuineFourPDEComponentBase D R G)
    (C : GenuineConstraintPropagationComponent D)
    (E : GenuineEnergyConditionPreservationComponent D R)
    (T : GenuineContinuationUpToCollapseThresholdComponent D R)
    (K : GenuineCollapseCriterionFromRestrictedSeedComponent D R) :
    GenuinePDEEstimateWitnessComponentsExist := by
  exact ⟨D, R, G,
    ⟨genuinePDEEstimateWitnessComponents_from_four_components B C E T K⟩⟩

def GenuineConstraintPropagationComponentExists : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
    Nonempty (GenuineConstraintPropagationComponent D)

def GenuineEnergyConditionPreservationComponentExists : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
    Nonempty (GenuineEnergyConditionPreservationComponent D R)

def GenuineContinuationUpToCollapseThresholdComponentExists : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
    Nonempty (GenuineContinuationUpToCollapseThresholdComponent D R)

def GenuineCollapseCriterionFromRestrictedSeedComponentExists : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
    Nonempty (GenuineCollapseCriterionFromRestrictedSeedComponent D R)

def GenuineFourPDEComponentExistenceReductionTarget : Prop :=
  ∃ D : FourDimensionalNonSymmetricEinsteinMatterData,
  ∃ R : ToolkitAdmissibleRegion D,
  ∃ G : GenuineEinsteinMatterDatum D,
    Nonempty (GenuineFourPDEComponentBase D R G) ∧
    Nonempty (GenuineConstraintPropagationComponent D) ∧
    Nonempty (GenuineEnergyConditionPreservationComponent D R) ∧
    Nonempty (GenuineContinuationUpToCollapseThresholdComponent D R) ∧
    Nonempty (GenuineCollapseCriterionFromRestrictedSeedComponent D R)

theorem genuinePDEEstimateWitnessComponentsExist_from_four_component_target
    (h : GenuineFourPDEComponentExistenceReductionTarget) :
    GenuinePDEEstimateWitnessComponentsExist := by
  rcases h with ⟨D, R, G, hB, hC, hE, hT, hK⟩
  rcases hB with ⟨B⟩
  rcases hC with ⟨C⟩
  rcases hE with ⟨E⟩
  rcases hT with ⟨T⟩
  rcases hK with ⟨K⟩
  exact genuinePDEEstimateWitnessComponentsExist_from_four_components B C E T K

end Frontier
end Chronos
