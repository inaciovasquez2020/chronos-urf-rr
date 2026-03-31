import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.Adjoint

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

noncomputable def Q (L Pi : V →ₗ[ℝ] V) : V →ₗ[ℝ] V :=
(L.adjoint.comp L) + Pi

axiom coercivity_Q :
  ∃ c > 0, ∀ x : V, ⟪(Q (LinearMap.id) (LinearMap.id)) x, x⟫ ≥ c * ‖x‖^2

end Chronos
