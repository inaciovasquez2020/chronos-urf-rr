import ChronosImports
<<<<<<< HEAD
import Mathlib.MeasureTheory.Integral.IntervalIntegral
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Data.Real.Basic

open Real MeasureTheory

variable {u : ℝ → ℝ}

def strain (t : ℝ) : ℝ := |u t|

def meanStrain (T : ℝ) : ℝ :=
(1/T) * ∫ t in (0)..T, strain t

def lyapunovEstimate (T : ℝ) : ℝ :=
Real.log (1 + T)

theorem IECP_conditional
  (T α : ℝ)
  (hT : T > 0)
  (hα : meanStrain T ≥ α)
  (hα1 : α ≤ 1) :
  lyapunovEstimate T ≥ Real.log (1 + α*T) := by
  unfold lyapunovEstimate
  have h₁ : 1 + T ≥ 1 + α*T := by
    have : T ≥ α*T := by
      have hT0 : T ≥ 0 := le_of_lt hT
      have : 1 ≥ α := by linarith
      nlinarith
    linarith
  have hpos₁ : 0 < 1 + α*T := by linarith
  exact Real.log_le_log hpos₁ h₁
=======
import Mathlib.Data.Real.Basic

open Real

def lyapunovEstimate (T : ℝ) : ℝ :=
Real.log (1 + T)
>>>>>>> 9586cd6 (Add URF Lean scaffolding modules)
