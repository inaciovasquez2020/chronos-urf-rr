import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Tactic

namespace Chronos.RapidityGeometry

theorem radial_density (l x : ℝ) :
    (Real.exp (-l) * Real.sinh x)^2 *
      |deriv (fun u : ℝ =>
          Real.exp (-u) * Real.cosh x) l *
        deriv (fun v : ℝ =>
          Real.exp (-l) * Real.sinh v) x -
        deriv (fun v : ℝ =>
          Real.exp (-l) * Real.cosh v) x *
        deriv (fun u : ℝ =>
          Real.exp (-u) * Real.sinh x) l| =
      Real.exp (-l)^4 * Real.sinh x^2 := by
  have he : HasDerivAt
      (fun u : ℝ => Real.exp (-u))
      (-Real.exp (-l)) l := by
    simpa [Function.comp_def] using
      (Real.hasDerivAt_exp (-l)).comp l
        ((hasDerivAt_id l).neg)
  have htl :
      deriv (fun u : ℝ =>
        Real.exp (-u) * Real.cosh x) l =
        -Real.exp (-l) * Real.cosh x :=
    (he.mul_const _).deriv
  have hrl :
      deriv (fun u : ℝ =>
        Real.exp (-u) * Real.sinh x) l =
        -Real.exp (-l) * Real.sinh x :=
    (he.mul_const _).deriv
  have htx :
      deriv (fun v : ℝ =>
        Real.exp (-l) * Real.cosh v) x =
        Real.exp (-l) * Real.sinh x :=
    ((Real.hasDerivAt_cosh x).const_mul _).deriv
  have hrx :
      deriv (fun v : ℝ =>
        Real.exp (-l) * Real.sinh v) x =
        Real.exp (-l) * Real.cosh x :=
    ((Real.hasDerivAt_sinh x).const_mul _).deriv
  rw [htl, hrl, htx, hrx]
  have hd :
      (-Real.exp (-l) * Real.cosh x) *
        (Real.exp (-l) * Real.cosh x) -
      (Real.exp (-l) * Real.sinh x) *
        (-Real.exp (-l) * Real.sinh x) =
      -(Real.exp (-l))^2 := by
    calc
      _ = -(Real.exp (-l))^2 *
          (Real.cosh x^2 - Real.sinh x^2) := by ring
      _ = _ := by
        rw [Real.cosh_sq_sub_sinh_sq, mul_one]
  rw [hd, abs_neg, abs_of_nonneg (sq_nonneg _)]
  ring

#print axioms radial_density

end Chronos.RapidityGeometry
