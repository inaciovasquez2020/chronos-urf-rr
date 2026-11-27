import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Tactic

open Set MeasureTheory

namespace Chronos.RapidityGeometry

theorem angular_integral_substitution
    (x z : ℝ)
    (hx : 0 < x)
    (hz : 0 < z)
    (g : ℝ → ℝ)
    (hg : IntervalIntegrable g volume (-1) 1) :
    IntervalIntegrable
      (fun e =>
        g ((Real.cosh e -
          Real.cosh x * Real.cosh z) /
          (Real.sinh x * Real.sinh z)) *
        (Real.sinh e /
          (Real.sinh x * Real.sinh z)))
      volume |x-z| (x+z) ∧
    (∫ e in |x-z|..(x+z),
        g ((Real.cosh e -
          Real.cosh x * Real.cosh z) /
          (Real.sinh x * Real.sinh z)) *
        (Real.sinh e /
          (Real.sinh x * Real.sinh z))) =
      ∫ u in (-1 : ℝ)..1, g u := by
  let D := Real.sinh x * Real.sinh z
  let f : ℝ → ℝ := fun e =>
    (Real.cosh e -
      Real.cosh x * Real.cosh z) / D
  let df : ℝ → ℝ := fun e =>
    Real.sinh e / D

  have hD : 0 < D :=
    mul_pos
      (Real.sinh_pos_iff.mpr hx)
      (Real.sinh_pos_iff.mpr hz)

  have hab : |x-z| ≤ x+z := by
    apply abs_le.mpr
    constructor <;> linarith

  have hf : Continuous f := by
    dsimp [f]
    exact
      (Real.continuous_cosh.sub
        continuous_const).div_const D

  have hderiv :
      ∀ v ∈ Ioo (min |x-z| (x+z))
                  (max |x-z| (x+z)),
        HasDerivAt f (df v) v := by
    intro v hv
    dsimp [f,df]
    exact
      ((Real.hasDerivAt_cosh v).sub_const
        (Real.cosh x * Real.cosh z)).div_const D

  have hnonneg :
      ∀ v ∈ Ioo (min |x-z| (x+z))
                  (max |x-z| (x+z)),
        0 ≤ df v := by
    intro v hv
    have hv' := hv.1
    rw [min_eq_left hab] at hv'
    have hv0 : 0 ≤ v :=
      (abs_nonneg (x-z)).trans hv'.le
    exact div_nonneg
      (Real.sinh_nonneg_iff.mpr hv0) hD.le

  have hlo : f |x-z| = -1 := by
    dsimp [f]
    rw [Real.cosh_abs, Real.cosh_sub]
    apply (div_eq_iff (ne_of_gt hD)).2
    dsimp [D]
    ring

  have hhi : f (x+z) = 1 := by
    dsimp [f]
    rw [Real.cosh_add]
    apply (div_eq_iff (ne_of_gt hD)).2
    dsimp [D]
    ring

  have hi :=
    intervalIntegral.integrable_comp_mul_deriv_iff_of_deriv_nonneg
      (f := f) (f' := df) (g := g)
      (a := |x-z|) (b := x+z)
      hf.continuousOn hderiv hnonneg

  have he :=
    intervalIntegral.integral_comp_mul_deriv_of_deriv_nonneg
      (f := f) (f' := df) (g := g)
      (a := |x-z|) (b := x+z)
      hf.continuousOn hderiv hnonneg

  rw [hlo,hhi] at hi he

  constructor
  · simpa only [Function.comp_apply, f, df, D]
      using hi.mpr hg
  · simpa only [Function.comp_apply, f, df, D]
      using he

#print axioms angular_integral_substitution

end Chronos.RapidityGeometry
