import Mathlib.Analysis.InnerProductSpace.Basic

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

noncomputable def Q (L : V → V) (Pi : V → V) : V → V :=
fun x => (LinearMap.adjoint (LinearMap.ofLinear L)) (L x) + Pi x

axiom coercivity_Q :
  ∃ c > 0, ∀ x : V, ⟪Q (fun x => x) (fun x => x) x, x⟫ ≥ c * ‖x‖^2

end Chronos
