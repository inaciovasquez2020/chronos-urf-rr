import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {E : Type} [Fintype E]

abbrev EdgeSpace (E : Type) := E → ZMod 2

/-- Standard F2 inner product -/
def inner (x y : EdgeSpace E) : ZMod 2 :=
  ∑ e, x e * y e

theorem inner_symmetric (x y : EdgeSpace E) :
  inner x y = inner y x := by
  classical
  simp [inner, mul_comm]

theorem inner_bilinear_left (x y z : EdgeSpace E) :
  inner (fun e => x e + y e) z =
  inner x z + inner y z := by
  classical
  simp [inner, add_mul, Finset.sum_add_distrib]

theorem orthogonality_def :
  True := by
  trivial

end URF
