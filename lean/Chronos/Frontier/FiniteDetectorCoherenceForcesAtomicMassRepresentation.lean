import Mathlib

namespace Chronos
namespace Frontier

open scoped BigOperators

/--
A finite detector extraction is coherent when it is calibrated on atoms,
vanishes on the empty detector family, and is additive over disjoint unions.

The extraction function is not defined to be a sum.  The representation theorem
below proves that every coherent extraction is forced to be the atomic finite
sum.  This removes the regrouping obstruction: no coherent finite detector
interface can depend on the chosen local presentation, ordering, or finite
blocking of the same atomic detector family.
-/
structure FiniteDetectorCoherentExtraction
    (Detector : Type*) [DecidableEq Detector] where
  atomMass : Detector → ℕ
  extract : Finset Detector → ℕ
  empty_zero : extract ∅ = 0
  disjoint_union :
    ∀ {A B : Finset Detector},
      Disjoint A B → extract (A ∪ B) = extract A + extract B
  singleton :
    ∀ d : Detector, extract {d} = atomMass d

/--
Coherence forces atomic mass representation.

This is not a definitional unfolding theorem.  The extraction map is arbitrary
subject to empty-zero, disjoint-additivity, and singleton calibration.  The
conclusion proves that these axioms uniquely determine extraction on every
finite detector family.
-/
theorem finiteDetectorCoherence_forces_atomicMassRepresentation
    {Detector : Type*} [DecidableEq Detector]
    (C : FiniteDetectorCoherentExtraction Detector) :
    ∀ A : Finset Detector, C.extract A = A.sum C.atomMass := by
  intro A
  refine Finset.induction_on A ?empty ?insert
  · simp [C.empty_zero]
  · intro a A ha ih
    have hdisj : Disjoint ({a} : Finset Detector) A := by
      rw [Finset.disjoint_left]
      intro x hx hA
      simp at hx
      subst x
      exact ha hA
    have hunion : ({a} : Finset Detector) ∪ A = insert a A := by
      ext x
      simp
    calc
      C.extract (insert a A)
          = C.extract (({a} : Finset Detector) ∪ A) := by
              rw [hunion]
      _ = C.extract ({a} : Finset Detector) + C.extract A := by
              exact C.disjoint_union hdisj
      _ = C.atomMass a + A.sum C.atomMass := by
              rw [C.singleton, ih]
      _ = (insert a A).sum C.atomMass := by
              rw [Finset.sum_insert ha]

/--
Uniqueness of coherent extraction.

Two coherent detector interfaces with the same atomic mass assignment have the
same extraction on every finite detector family.
-/
theorem finiteDetectorCoherence_uniqueExtraction
    {Detector : Type*} [DecidableEq Detector]
    (C₁ C₂ : FiniteDetectorCoherentExtraction Detector)
    (hMass : C₁.atomMass = C₂.atomMass) :
    C₁.extract = C₂.extract := by
  funext A
  rw [finiteDetectorCoherence_forces_atomicMassRepresentation C₁,
      finiteDetectorCoherence_forces_atomicMassRepresentation C₂]
  simp [hMass]

/--
Pointwise form of uniqueness, suitable for downstream bridge use.
-/
theorem finiteDetectorCoherence_noRegroupingObstruction
    {Detector : Type*} [DecidableEq Detector]
    (C₁ C₂ : FiniteDetectorCoherentExtraction Detector)
    (hMass : C₁.atomMass = C₂.atomMass)
    (A : Finset Detector) :
    C₁.extract A = C₂.extract A := by
  exact congrFun (finiteDetectorCoherence_uniqueExtraction C₁ C₂ hMass) A

end Frontier
end Chronos
