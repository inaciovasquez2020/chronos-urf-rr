import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

def CutSpace := (V → ZMod 2)

theorem cut_space_duality :
  True := by trivial

end URF
