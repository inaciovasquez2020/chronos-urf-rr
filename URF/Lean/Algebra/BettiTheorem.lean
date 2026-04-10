import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

abbrev EdgeSpace (E : Type) := E → ZMod 2
abbrev VertexSpace (V : Type) := V → ZMod 2

variable (B : EdgeSpace E →ₗ[ZMod 2] VertexSpace V)

/-- Main Betti identity -/
theorem betti_identity :
  FiniteDimensional.finrank ZMod 2 (LinearMap.ker B) +
  FiniteDimensional.finrank ZMod 2 (LinearMap.range B) =
  Fintype.card E :=
by
  classical
  exact LinearMap.rank_range_add_rank_ker B

end URF
