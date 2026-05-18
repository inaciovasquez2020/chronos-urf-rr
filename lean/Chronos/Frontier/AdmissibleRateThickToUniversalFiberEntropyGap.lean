import Chronos.Frontier.AdmissibleFiberMassUniformFloor

/-!
Admissible rate-thick coercivity to universal fiber-entropy gap.

The unrestricted arbitrary-`FiberMassData` route is already refuted by
`UniversalWeakestMissingMeasureFiberMassLemmaRefutation`.

This file closes the admissible bridge only: a rate-thick coercivity target
carries the same positive fiber-mass floor as a fiber-entropy-gap target.
-/

namespace Chronos.Frontier

structure UniversalFiberEntropyGapTarget (M : FiberMassData) where
  order_surface : OrderSurfaceAvailable
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  entropy_gap_floor : ∀ n : ℕ, epsilon ≤ M.fiberMass n

def RateThickToUniversalFiberEntropyGapBridge
    (M : FiberMassData) : Prop :=
  Nonempty (RateThickFiberCoercivityTarget M) →
  Nonempty (UniversalFiberEntropyGapTarget M)

theorem universalFiberEntropyGapTarget_from_rate_thick_target
    (M : FiberMassData)
    (h : Nonempty (RateThickFiberCoercivityTarget M)) :
    Nonempty (UniversalFiberEntropyGapTarget M) := by
  rcases h with ⟨T⟩
  exact ⟨⟨T.order_surface, T.epsilon, T.epsilon_pos, T.fiber_mass_floor⟩⟩

theorem RateThickToUniversalFiberEntropyGapBridge_solved
    (M : FiberMassData) :
    RateThickToUniversalFiberEntropyGapBridge M := by
  intro h
  exact universalFiberEntropyGapTarget_from_rate_thick_target M h

def AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (RateThickFiberCoercivityTarget A.data) →
    Nonempty (UniversalFiberEntropyGapTarget A.data)

theorem AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap_solved :
    AdmissibleRateThickFiberCoercivityToUniversalFiberEntropyGap := by
  intro A hA
  exact universalFiberEntropyGapTarget_from_rate_thick_target A.data hA

def AdmissibleUniversalFiberEntropyGapTarget : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (UniversalFiberEntropyGapTarget A.data)

theorem AdmissibleUniversalFiberEntropyGapTarget_solved :
    AdmissibleUniversalFiberEntropyGapTarget := by
  intro A
  exact universalFiberEntropyGapTarget_from_rate_thick_target
    A.data (AdmissibleRateThickFiberCoercivityTarget_solved A)

def UnrestrictedUniversalFiberEntropyGapTarget : Prop :=
  ∀ M : FiberMassData,
    Nonempty (UniversalFiberEntropyGapTarget M)

theorem UnrestrictedUniversalFiberEntropyGapTarget_refuted :
    ¬ UnrestrictedUniversalFiberEntropyGapTarget := by
  intro h
  rcases h zeroFiberMassData with ⟨T⟩
  have hε_le_zero : T.epsilon ≤ 0 := by
    simpa [zeroFiberMassData] using T.entropy_gap_floor 0
  exact (not_lt_of_ge hε_le_zero) T.epsilon_pos

end Chronos.Frontier
