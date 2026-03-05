import ChronosImports
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

open Real

def entropyDepth (n : ℕ) : ℝ :=
(n : ℝ) * Real.log (n + 1)

theorem entropyDepth_lower_bound
  (n : ℕ) (h : n ≥ 2) :
  entropyDepth n ≥ (n : ℝ) := by
  unfold entropyDepth
  have h1 : Real.log (n+1) ≥ 1 := by
    have : (n+1 : ℝ) ≥ Real.exp 1 := by
      have : (n : ℝ) ≥ 2 := by exact_mod_cast h
      linarith
    exact Real.log_le_iff_le_exp.mpr this
  nlinarith

theorem amplification_step (n : ℕ) :
  entropyDepth (2*n) ≥ entropyDepth n := by
  unfold entropyDepth
  have h :
    Real.log (2*n+1) ≥ Real.log (n+1) := by
      apply Real.log_le_log
      positivity
      linarith
  nlinarith
