import ChronosImports
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

def entropyDepth (n : ℕ) : ℝ :=
(n : ℝ) * Real.log (n + 1)
