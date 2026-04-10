import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

theorem rank_nullity
  (B : (E → ZMod 2) →ₗ[ZMod 2] (V → ZMod 2)) :
  FiniteDimensional.finrank ZMod 2 B.ker +
  FiniteDimensional.finrank ZMod 2 B.range =
  Fintype.card E :=
by
  classical
  exact LinearMap.rank_range_add_rank_ker B

end URF
