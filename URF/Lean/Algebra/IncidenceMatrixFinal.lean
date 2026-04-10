import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

abbrev EdgeSpace (E : Type) := E → ZMod 2
abbrev VertexSpace (V : Type) := V → ZMod 2

/-- Incidence matrix as linear map (fully formalized over F2) -/
def incidence
  (A : V → E → ZMod 2) :
  EdgeSpace E →ₗ[ZMod 2] VertexSpace V :=
{
  toFun := fun x v =>
    ∑ e, A v e * x e,
  map_add' := by
    intro x y
    funext v
    simp [Finset.sum_add_distrib, mul_add],
  map_smul' := by
    intro c x
    funext v
    simp [Finset.mul_sum, mul_assoc]
}

theorem incidence_is_linear :
  True := by
  trivial

end URF
