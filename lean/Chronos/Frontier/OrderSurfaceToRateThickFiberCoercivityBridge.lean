import Chronos.Frontier.DomainIndexedPositiveEntropyOrder

/-!
Order-surface to rate-thick fiber coercivity bridge.

This file proves the exact bridge available from the merged
domain-indexed positive-entropy order surface.

The remaining mathematical obstruction is not an order-surface obstruction.
It is the uniform measure/fiber-mass floor.
-/

namespace Chronos.Frontier

structure FiberMassData where
  fiberMass : ℕ → ℝ

def OrderSurfaceAvailable : Prop :=
  DomainIndexedPositiveEntropyWitnessConstruction_order.{0,0} True

def FiberMassUniformFloor (M : FiberMassData) : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ n : ℕ, ε ≤ M.fiberMass n

structure RateThickFiberCoercivityTarget (M : FiberMassData) where
  order_surface : OrderSurfaceAvailable
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  fiber_mass_floor : ∀ n : ℕ, epsilon ≤ M.fiberMass n

def OrderSurfaceToRateThickFiberCoercivityBridge
    (M : FiberMassData) : Prop :=
  OrderSurfaceAvailable →
  FiberMassUniformFloor M →
  Nonempty (RateThickFiberCoercivityTarget M)

def WeakestMissingMeasureFiberMassLemma
    (M : FiberMassData) : Prop :=
  FiberMassUniformFloor M

def UniversalWeakestMissingMeasureFiberMassLemma : Prop :=
  ∀ M : FiberMassData, WeakestMissingMeasureFiberMassLemma M

def UnrestrictedRateThickFiberCoercivityTarget : Prop :=
  ∀ M : FiberMassData, Nonempty (RateThickFiberCoercivityTarget M)

theorem order_surface_available_solved :
    OrderSurfaceAvailable := by
  exact DomainIndexedPositiveEntropyWitnessConstruction_order_solved True

theorem exact_coercivity_target_from_measure_fiber_mass_floor
    (M : FiberMassData)
    (hOrder : OrderSurfaceAvailable)
    (hFloor : FiberMassUniformFloor M) :
    Nonempty (RateThickFiberCoercivityTarget M) := by
  rcases hFloor with ⟨ε, hε, hMass⟩
  exact ⟨⟨hOrder, ε, hε, hMass⟩⟩

theorem OrderSurfaceToRateThickFiberCoercivityBridge_solved
    (M : FiberMassData) :
    OrderSurfaceToRateThickFiberCoercivityBridge M := by
  intro hOrder hFloor
  exact exact_coercivity_target_from_measure_fiber_mass_floor M hOrder hFloor

theorem unrestricted_rate_thick_reduced_to_measure_fiber_mass_floor
    (hFloor : UniversalWeakestMissingMeasureFiberMassLemma) :
    UnrestrictedRateThickFiberCoercivityTarget := by
  intro M
  exact exact_coercivity_target_from_measure_fiber_mass_floor
    M order_surface_available_solved (hFloor M)

end Chronos.Frontier
