import Mathlib.LinearAlgebra.FiniteDimensional

namespace URF

variable {V E : Type} [Fintype V] [Fintype E]

abbrev EdgeSpace (E : Type) := E → ZMod 2
abbrev VertexSpace (V : Type) := V → ZMod 2

variable (B : EdgeSpace E →ₗ[ZMod 2] VertexSpace V)

/-- Cycle space defined as kernel of boundary map -/
def CycleSpace := LinearMap.ker B

/-- Kernel equals cycle space (definition closure) -/
theorem kernel_eq_cycleSpace :
  CycleSpace B = LinearMap.ker B :=
by
  rfl

/-- Membership characterization -/
theorem mem_cycleSpace_iff :
  ∀ x, x ∈ CycleSpace B ↔ B x = 0 :=
by
  intro x
  rfl

end URF
