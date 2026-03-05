import ChronosImports
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Data.Real.Basic

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def kinetic (ψ : H) : ℝ := ‖ψ‖^2
