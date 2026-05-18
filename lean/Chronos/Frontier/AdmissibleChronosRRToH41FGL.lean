import Chronos.Frontier.AdmissibleUniversalFiberEntropyGapToChronosRR

/-!
Admissible Chronos-RR target to H4.1/FGL target.

This closes only the admissible target-level bridge. It does not assert
unrestricted Chronos-RR or theorem-level H4.1/FGL. The unrestricted
arbitrary-`FiberMassData` target is refuted by the zero fiber-mass object.
-/

namespace Chronos.Frontier

structure H41FGLTarget (M : FiberMassData) where
  order_surface : OrderSurfaceAvailable
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  h41_fgl_floor : ∀ n : ℕ, epsilon ≤ M.fiberMass n

def ChronosRRToH41FGLBridge
    (M : FiberMassData) : Prop :=
  Nonempty (ChronosRRTarget M) →
  Nonempty (H41FGLTarget M)

theorem h41FGLTarget_from_chronosRRTarget
    (M : FiberMassData)
    (h : Nonempty (ChronosRRTarget M)) :
    Nonempty (H41FGLTarget M) := by
  rcases h with ⟨R⟩
  exact ⟨⟨R.order_surface, R.epsilon, R.epsilon_pos, R.chronos_rr_floor⟩⟩

theorem ChronosRRToH41FGLBridge_solved
    (M : FiberMassData) :
    ChronosRRToH41FGLBridge M := by
  intro h
  exact h41FGLTarget_from_chronosRRTarget M h

def AdmissibleChronosRRToH41FGL : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (ChronosRRTarget A.data) →
    Nonempty (H41FGLTarget A.data)

theorem AdmissibleChronosRRToH41FGL_solved :
    AdmissibleChronosRRToH41FGL := by
  intro A hA
  exact h41FGLTarget_from_chronosRRTarget A.data hA

def AdmissibleH41FGLTarget : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (H41FGLTarget A.data)

theorem AdmissibleH41FGLTarget_solved :
    AdmissibleH41FGLTarget := by
  intro A
  exact h41FGLTarget_from_chronosRRTarget
    A.data (AdmissibleChronosRRTarget_solved A)

def UnrestrictedH41FGLTarget : Prop :=
  ∀ M : FiberMassData,
    Nonempty (H41FGLTarget M)

theorem UnrestrictedH41FGLTarget_refuted :
    ¬ UnrestrictedH41FGLTarget := by
  intro h
  rcases h zeroFiberMassData with ⟨T⟩
  have hε_le_zero : T.epsilon ≤ 0 := by
    simpa [zeroFiberMassData] using T.h41_fgl_floor 0
  exact (not_lt_of_ge hε_le_zero) T.epsilon_pos

end Chronos.Frontier
