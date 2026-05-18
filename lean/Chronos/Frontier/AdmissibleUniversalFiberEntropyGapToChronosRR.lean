import Chronos.Frontier.AdmissibleRateThickToUniversalFiberEntropyGap

/-!
Admissible universal fiber-entropy gap to Chronos-RR target.

This closes only the admissible target-level bridge. It does not assert
unrestricted Chronos-RR, and the unrestricted arbitrary-`FiberMassData`
target is refuted by the zero fiber-mass object.
-/

namespace Chronos.Frontier

structure ChronosRRTarget (M : FiberMassData) where
  order_surface : OrderSurfaceAvailable
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  chronos_rr_floor : ∀ n : ℕ, epsilon ≤ M.fiberMass n

def UniversalFiberEntropyGapToChronosRRBridge
    (M : FiberMassData) : Prop :=
  Nonempty (UniversalFiberEntropyGapTarget M) →
  Nonempty (ChronosRRTarget M)

theorem chronosRRTarget_from_universalFiberEntropyGapTarget
    (M : FiberMassData)
    (h : Nonempty (UniversalFiberEntropyGapTarget M)) :
    Nonempty (ChronosRRTarget M) := by
  rcases h with ⟨G⟩
  exact ⟨⟨G.order_surface, G.epsilon, G.epsilon_pos, G.entropy_gap_floor⟩⟩

theorem UniversalFiberEntropyGapToChronosRRBridge_solved
    (M : FiberMassData) :
    UniversalFiberEntropyGapToChronosRRBridge M := by
  intro h
  exact chronosRRTarget_from_universalFiberEntropyGapTarget M h

def AdmissibleUniversalFiberEntropyGapToChronosRR : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (UniversalFiberEntropyGapTarget A.data) →
    Nonempty (ChronosRRTarget A.data)

theorem AdmissibleUniversalFiberEntropyGapToChronosRR_solved :
    AdmissibleUniversalFiberEntropyGapToChronosRR := by
  intro A hA
  exact chronosRRTarget_from_universalFiberEntropyGapTarget A.data hA

def AdmissibleChronosRRTarget : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (ChronosRRTarget A.data)

theorem AdmissibleChronosRRTarget_solved :
    AdmissibleChronosRRTarget := by
  intro A
  exact chronosRRTarget_from_universalFiberEntropyGapTarget
    A.data (AdmissibleUniversalFiberEntropyGapTarget_solved A)

def UnrestrictedChronosRRTarget : Prop :=
  ∀ M : FiberMassData,
    Nonempty (ChronosRRTarget M)

theorem UnrestrictedChronosRRTarget_refuted :
    ¬ UnrestrictedChronosRRTarget := by
  intro h
  rcases h zeroFiberMassData with ⟨T⟩
  have hε_le_zero : T.epsilon ≤ 0 := by
    simpa [zeroFiberMassData] using T.chronos_rr_floor 0
  exact (not_lt_of_ge hε_le_zero) T.epsilon_pos

end Chronos.Frontier
