import Mathlib
import Chronos.Frontier.UnconditionalUniversalFiberEntropyGapObstruction

namespace Chronos
namespace Frontier

/--
Finite positive fiber-mass data.

The fiber type is finite and nonempty, and every active fiber has strictly
positive mass.
-/
structure FiniteSupportPositiveFiberMass where
  Fiber : Type
  fiberFintype : Fintype Fiber
  fiberNonempty : Nonempty Fiber
  mass : Fiber → ℝ
  mass_pos : ∀ x : Fiber, 0 < mass x

/--
Uniform positive floor on finite positive support.
-/
def FiniteSupportFiberMassUniformFloor
    (D : FiniteSupportPositiveFiberMass) : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ x : D.Fiber, ε ≤ D.mass x

/--
Finite positive support gives a uniform positive fiber-mass floor by taking
the minimum over the finite active fiber set.
-/
theorem finite_support_fiber_mass_uniform_floor
    (D : FiniteSupportPositiveFiberMass) :
    FiniteSupportFiberMassUniformFloor D := by
  classical
  letI : Fintype D.Fiber := D.fiberFintype
  let s : Finset ℝ := Finset.univ.image D.mass
  have hs : s.Nonempty := by
    rcases D.fiberNonempty with ⟨x⟩
    exact ⟨D.mass x, by simp [s]⟩
  refine ⟨s.min' hs, ?_, ?_⟩
  · have hmem : s.min' hs ∈ s := Finset.min'_mem s hs
    rcases Finset.mem_image.mp hmem with ⟨x, _hx, hx⟩
    rw [← hx]
    exact D.mass_pos x
  · intro x
    have hx : D.mass x ∈ s := by
      simp [s]
    exact Finset.min'_le s (D.mass x) hx

/--
Restricted rate-thick coercivity surface induced by a finite-support floor.
-/
def RestrictedRateThickFiberCoercivityFromFiniteSupport
    (D : FiniteSupportPositiveFiberMass) : Prop :=
  FiniteSupportFiberMassUniformFloor D

/--
Finite support feeds the restricted rate-thick coercivity surface.
-/
theorem restricted_rate_thick_fiber_coercivity_from_finite_support
    (D : FiniteSupportPositiveFiberMass) :
    RestrictedRateThickFiberCoercivityFromFiniteSupport D := by
  exact finite_support_fiber_mass_uniform_floor D

/--
Restricted UniversalFiberEntropyGap surface induced by finite positive
support.

This is restricted-domain only and does not contradict the unconditional
obstruction for arbitrary fiber-mass data.
-/
def RestrictedUniversalFiberEntropyGapFromFiniteSupport
    (D : FiniteSupportPositiveFiberMass) : Prop :=
  RestrictedRateThickFiberCoercivityFromFiniteSupport D

/--
Finite positive support gives restricted UniversalFiberEntropyGap through
the uniform floor/coercivity route.
-/
theorem restricted_universal_fiber_entropy_gap_from_finite_support
    (D : FiniteSupportPositiveFiberMass) :
    RestrictedUniversalFiberEntropyGapFromFiniteSupport D := by
  exact restricted_rate_thick_fiber_coercivity_from_finite_support D

end Frontier
end Chronos
