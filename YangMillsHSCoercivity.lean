import ChronosImports
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Data.Real.Basic

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

def kinetic (ψ : H) : ℝ := ‖ψ‖^2
def potential (ψ : H) : ℝ := ‖ψ‖
def YM_H (ψ : H) : ℝ := kinetic ψ + potential ψ

theorem coercivity_bound (ψ : H) :
  YM_H ψ ≥ ‖ψ‖^2 := by
  unfold YM_H kinetic potential
  have : ‖ψ‖ ≥ 0 := norm_nonneg ψ
  nlinarith
