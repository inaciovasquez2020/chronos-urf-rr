import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

def isConnected (G : Type) : Prop := True

theorem rank_boundary_eq_vertices_minus_components
  (B : (E → ZMod 2) →ₗ[ZMod 2] (V → ZMod 2))
  (c : Nat) :
  FiniteDimensional.finrank ZMod 2 B.range = Fintype.card V - c :=
by
  admit

end URF
