import Chronos.Frontier.OrderSurfaceToRateThickFiberCoercivityBridge

/-!
Refutation of the unrestricted universal measure/fiber-mass floor.

The bridge from PR #361 correctly isolated the weakest missing lemma:

  UniversalWeakestMissingMeasureFiberMassLemma

For arbitrary `FiberMassData`, that lemma is false. The zero fiber-mass
object has no positive uniform lower floor.
-/

namespace Chronos.Frontier

def zeroFiberMassData : FiberMassData where
  fiberMass := fun _ => 0

theorem zeroFiberMassData_no_uniform_floor :
    ¬ FiberMassUniformFloor zeroFiberMassData := by
  intro h
  rcases h with ⟨ε, hε_pos, hε_floor⟩
  have hε_le_zero : ε ≤ 0 := by
    simpa [zeroFiberMassData] using hε_floor 0
  exact (not_lt_of_ge hε_le_zero) hε_pos

theorem UniversalWeakestMissingMeasureFiberMassLemma_refuted :
    ¬ UniversalWeakestMissingMeasureFiberMassLemma := by
  intro h
  exact zeroFiberMassData_no_uniform_floor (h zeroFiberMassData)

theorem UnrestrictedRateThickFiberCoercivityTarget_refuted :
    ¬ UnrestrictedRateThickFiberCoercivityTarget := by
  intro h
  rcases h zeroFiberMassData with ⟨T⟩
  have hε_le_zero : T.epsilon ≤ 0 := by
    simpa [zeroFiberMassData] using T.fiber_mass_floor 0
  exact (not_lt_of_ge hε_le_zero) T.epsilon_pos

def RestrictedMeasureFiberMassFloorTarget : Prop :=
  ∀ M : FiberMassData,
    FiberMassUniformFloor M →
    Nonempty (RateThickFiberCoercivityTarget M)

theorem RestrictedMeasureFiberMassFloorTarget_solved :
    RestrictedMeasureFiberMassFloorTarget := by
  intro M hM
  exact exact_coercivity_target_from_measure_fiber_mass_floor
    M order_surface_available_solved hM

end Chronos.Frontier
