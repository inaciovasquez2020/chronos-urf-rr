import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Tactic

open Set MeasureTheory

namespace Chronos.RapidityGeometry

theorem exp_interval_substitution
    (a b : ℝ) (g : ℝ → ℝ) :
    (∫ x in a..b,
      g (Real.exp x) * Real.exp x) =
    ∫ u in (Real.exp a)..(Real.exp b), g u := by
  have h :=
    intervalIntegral.integral_comp_mul_deriv_of_deriv_nonneg
      (f := Real.exp)
      (f' := Real.exp)
      (g := g)
      (a := a)
      (b := b)
      Real.continuous_exp.continuousOn
      (fun x _ => Real.hasDerivAt_exp x)
      (fun x _ => (Real.exp_pos x).le)
  simpa only [Function.comp_apply] using h

theorem null_log_triangle_substitution
    (L : ℝ) (g : ℝ → ℝ → ℝ) :
    (∫ a in L..0,
      (∫ b in L..a,
        g (Real.exp a) (Real.exp b) *
          Real.exp b) * Real.exp a) =
    ∫ u in (Real.exp L)..1,
      ∫ v in (Real.exp L)..u, g u v := by
  have hinner (a : ℝ) :
      (∫ b in L..a,
        g (Real.exp a) (Real.exp b) *
          Real.exp b) =
      ∫ v in (Real.exp L)..(Real.exp a),
        g (Real.exp a) v :=
    exp_interval_substitution L a (g (Real.exp a))
  calc
    _ = (∫ a in L..0,
          (∫ v in (Real.exp L)..(Real.exp a),
            g (Real.exp a) v) *
              Real.exp a) := by
          simp_rw [hinner]
    _ = _ := by
      simpa only [Real.exp_zero] using
        (exp_interval_substitution L 0
          (fun u =>
            ∫ v in (Real.exp L)..u, g u v))

#print axioms exp_interval_substitution
#print axioms null_log_triangle_substitution

end Chronos.RapidityGeometry
