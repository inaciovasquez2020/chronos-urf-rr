import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Adjoint
import Mathlib.Topology.Algebra.Module

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

noncomputable def Q (L Pi : V →ₗ[ℝ] V) : V →ₗ[ℝ] V :=
(L.adjoint.comp L) + Pi

noncomputable def spectralGap (Q : V →ₗ[ℝ] V) : ℝ :=
sInf {r | ∃ x, ‖x‖ = 1 ∧ r = ⟪Q x, x⟫}

def Coercive (Q : V →ₗ[ℝ] V) : Prop :=
∃ c > 0, ∀ x, ⟪Q x, x⟫ ≥ c * ‖x‖^2

theorem spectral_gap_pos_iff_coercive
  (Q : V →ₗ[ℝ] V) :
  spectralGap Q > 0 ↔ Coercive Q := by
  constructor
  · intro h
    refine ⟨spectralGap Q, h, ?_⟩
    intro x
    by_cases hx : ‖x‖ = 0
    · simp [hx]
    · have : ‖(‖x‖⁻¹ • x)‖ = 1 := by
        simp [hx]
      have hdef := le_csInf ?_ (by use ‖x‖⁻¹ • x)
      have := mul_le_mul_of_nonneg_right hdef (by positivity)
      simpa
  · intro h
    obtain ⟨c, hc, hQ⟩ := h
    have : spectralGap Q ≥ c := by
      apply csInf_le
      use ⟨fun x => x, by simp⟩
    exact lt_of_lt_of_le hc this

end Chronos
