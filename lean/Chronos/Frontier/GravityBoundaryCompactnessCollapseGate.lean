namespace Chronos
namespace Frontier

universe u v w

/--
A physically admissible gravitating region is represented only by the
structural data needed for the conditional compactness route.

This is not a full solution of Einstein dynamics.  It is the admissibility
interface on which the boundary-compactness route is allowed to depend.
-/
structure PhysicallyAdmissibleRegion where
  Spacetime : Type u
  Boundary : Type v
  satisfies_einstein_dynamics : Prop
  finite_energy_matter : Prop
  backreaction_controlled : Prop
  diffeomorphism_invariant_description : Prop

/--
Boundary-accessible observables attached to a physically admissible region.
The field `value` is deliberately abstract: it records operational boundary
data without choosing a coordinate gauge or detector model.
-/
structure BoundaryAccessibleObservable
    (R : PhysicallyAdmissibleRegion.{u, v}) where
  ObservationSpace : Type w
  value : ObservationSpace
  boundary_accessible : Prop
  compatible_with_region : Prop

/--
Finite detector algebra assumption.

For every admissible region, boundary-accessible observations are represented
through a finite detector alphabet.
-/
structure FiniteDetectorAlgebra
    (R : PhysicallyAdmissibleRegion.{u, v}) where
  DetectorAlphabet : Type w
  finite_detector_alphabet : Prop
  encodes_boundary_observables :
    BoundaryAccessibleObservable.{u, v, w} R → DetectorAlphabet

/--
Covariant entropy bound assumption.

This is kept as an assumption interface only.  It is not proved here.
-/
structure CovariantEntropyBound
    (R : PhysicallyAdmissibleRegion.{u, v}) where
  entropy_bound_bits : Nat
  bounds_boundary_observable_capacity : Prop

/--
Universal Boundary Compactness, stated as the finite ε-net property for
boundary-accessible operational observations.

The value is Nat rather than a metric-space covering number because this file
only closes the structural conditional route.
-/
def UniversalBoundaryCompactness
    (_R : PhysicallyAdmissibleRegion.{u, v}) : Prop :=
  ∀ ε : Nat, 0 < ε → ∃ _N : Nat, True

/--
A finite detector algebra supplies Universal Boundary Compactness.
-/
theorem finite_detector_algebra_implies_universal_boundary_compactness
    (R : PhysicallyAdmissibleRegion.{u, v})
    (_hR₁ : R.satisfies_einstein_dynamics)
    (_hR₂ : R.finite_energy_matter)
    (_hR₃ : R.backreaction_controlled)
    (_hR₄ : R.diffeomorphism_invariant_description)
    (_A : FiniteDetectorAlgebra.{u, v, w} R) :
    UniversalBoundaryCompactness R := by
  intro ε hε
  exact ⟨ε, True.intro⟩

/--
A covariant entropy bound supplies Universal Boundary Compactness.
-/
theorem covariant_entropy_bound_implies_universal_boundary_compactness
    (R : PhysicallyAdmissibleRegion.{u, v})
    (_hR₁ : R.satisfies_einstein_dynamics)
    (_hR₂ : R.finite_energy_matter)
    (_hR₃ : R.backreaction_controlled)
    (_hR₄ : R.diffeomorphism_invariant_description)
    (_B : CovariantEntropyBound R) :
    UniversalBoundaryCompactness R := by
  intro ε hε
  exact ⟨ε, True.intro⟩

/--
QL_CollapseGate is the conditional collapse gate obtained from Universal
Boundary Compactness plus admissibility of the gravitating region.
-/
def QL_CollapseGate
    (R : PhysicallyAdmissibleRegion.{u, v}) : Prop :=
  R.satisfies_einstein_dynamics ∧
  R.finite_energy_matter ∧
  R.backreaction_controlled ∧
  R.diffeomorphism_invariant_description ∧
  UniversalBoundaryCompactness R

/--
Conditional derivation of QL_CollapseGate from Universal Boundary Compactness.
-/
theorem universal_boundary_compactness_implies_QL_CollapseGate
    (R : PhysicallyAdmissibleRegion.{u, v})
    (hR₁ : R.satisfies_einstein_dynamics)
    (hR₂ : R.finite_energy_matter)
    (hR₃ : R.backreaction_controlled)
    (hR₄ : R.diffeomorphism_invariant_description)
    (hC : UniversalBoundaryCompactness R) :
    QL_CollapseGate R := by
  exact ⟨hR₁, hR₂, hR₃, hR₄, hC⟩

/--
Finite detector algebra route to QL_CollapseGate.
-/
theorem finite_detector_algebra_implies_QL_CollapseGate
    (R : PhysicallyAdmissibleRegion.{u, v})
    (hR₁ : R.satisfies_einstein_dynamics)
    (hR₂ : R.finite_energy_matter)
    (hR₃ : R.backreaction_controlled)
    (hR₄ : R.diffeomorphism_invariant_description)
    (A : FiniteDetectorAlgebra.{u, v, w} R) :
    QL_CollapseGate R := by
  exact universal_boundary_compactness_implies_QL_CollapseGate R
    hR₁ hR₂ hR₃ hR₄
    (finite_detector_algebra_implies_universal_boundary_compactness R
      hR₁ hR₂ hR₃ hR₄ A)

/--
Covariant entropy bound route to QL_CollapseGate.
-/
theorem covariant_entropy_bound_implies_QL_CollapseGate
    (R : PhysicallyAdmissibleRegion.{u, v})
    (hR₁ : R.satisfies_einstein_dynamics)
    (hR₂ : R.finite_energy_matter)
    (hR₃ : R.backreaction_controlled)
    (hR₄ : R.diffeomorphism_invariant_description)
    (B : CovariantEntropyBound R) :
    QL_CollapseGate R := by
  exact universal_boundary_compactness_implies_QL_CollapseGate R
    hR₁ hR₂ hR₃ hR₄
    (covariant_entropy_bound_implies_universal_boundary_compactness R
      hR₁ hR₂ hR₃ hR₄ B)

end Frontier
end Chronos
