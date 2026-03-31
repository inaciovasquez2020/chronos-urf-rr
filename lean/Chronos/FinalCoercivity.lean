import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Adjoint

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

noncomputable def Q (L Pi : V →ₗ[ℝ] V) : V →ₗ[ℝ] V :=
(L.adjoint.comp L) + Pi

theorem coercivity_Q_id :
  ∃ c > 0, ∀ x : V, ⟪(Q LinearMap.id LinearMap.id) x, x⟫ ≥ c * ‖x‖^2 := by
  refine ⟨1, by decide, ?_⟩
  intro x
  have h1 : ⟪(LinearMap.id : V →ₗ[ℝ] V) x, x⟫ = ‖x‖^2 := by
    simpa using inner_self_eq_norm_sq x
  have h2 : ⟪((LinearMap.id.adjoint.comp LinearMap.id) x), x⟫ = ‖x‖^2 := by
    simpa using inner_self_eq_norm_sq x
  have : ⟪(Q LinearMap.id LinearMap.id) x, x⟫ = 2 * ‖x‖^2 := by
    simp [Q, h1, h2]
  simpa [this]

end Chronos
