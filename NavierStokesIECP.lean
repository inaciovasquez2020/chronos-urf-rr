import ChronosImports
import Mathlib.Data.Real.Basic

open Real

def lyapunovEstimate (T : ℝ) : ℝ :=
Real.log (1 + T)
