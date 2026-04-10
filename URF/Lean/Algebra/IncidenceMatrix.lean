import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable (V E : Type) [Fintype V] [Fintype E]

def C0 := V → ZMod 2
def C1 := E → ZMod 2

variable (G : Type)

structure IncidenceData :=
  (head tail : E → V)

def boundary (I : IncidenceData V E) : C1 V E → C0 V :=
  fun x v =>
    ∑ e, x e * ((if v = I.head e then 1 else 0) + (if v = I.tail e then 1 else 0))

end URF
