import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Adjoint

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

noncomputable def Q (L Pi : V →ₗ[ℝ] V) : V →ₗ[ℝ] V :=
(L.adjoint.comp L) + Pi

def Coercive (Pi : V →ₗ[ℝ] V) : Prop :=
∃ c > 0, ∀ x, ⟪Pi x, x⟫ ≥ c * ‖x‖^2

theorem coercivity_Q
  (L Pi : V →ₗ[ℝ] V)
  (hPi : Coercive Pi) :
  ∃ c > 0, ∀ x : V, ⟪(Q L Pi) x, x⟫ ≥ c * ‖x‖^2 := by
  obtain ⟨c₀, hc₀pos, hPi_lb⟩ := hPi
  refine ⟨c₀, hc₀pos, ?_⟩
  intro x
  have hL : 0 ≤ ⟪(L.adjoint.comp L) x, x⟫ := by
    have : ⟪L x, L x⟫ = ⟪(L.adjoint.comp L) x, x⟫ := by simp
    simpa [this] using inner_self_nonneg (L x)
  have hPi' := hPi_lb x
  have : ⟪(Q L Pi) x, x⟫ =
      ⟪(L.adjoint.comp L) x, x⟫ + ⟪Pi x, x⟫ := by
    simp [Q]
  have hsum : ⟪(Q L Pi) x, x⟫ ≥ c₀ * ‖x‖^2 := by
    have := add_le_add hL hPi'
    simpa [this]
  simpa using hsum

end Chronos
