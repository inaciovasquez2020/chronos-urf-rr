import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Tactic

namespace Chronos.RapidityGeometry

theorem angular_density
    (x z e : ℝ)
    (hx : 0 < Real.sinh x)
    (hz : 0 < Real.sinh z)
    (he : 0 < Real.sinh e) :
    Real.sinh x^2 * Real.sinh z^2 *
      |deriv (fun v : ℝ =>
        (Real.cosh x * Real.cosh z - Real.cosh v) /
        (Real.sinh x * Real.sinh z)) e| =
      Real.sinh x * Real.sinh z * Real.sinh e := by
  have hc : HasDerivAt
      (fun v : ℝ =>
        Real.cosh x * Real.cosh z - Real.cosh v)
      (-Real.sinh e) e := by
    simpa using
      (hasDerivAt_const e
        (Real.cosh x * Real.cosh z)).sub
          (Real.hasDerivAt_cosh e)
  have hd :
      deriv (fun v : ℝ =>
        (Real.cosh x * Real.cosh z - Real.cosh v) /
        (Real.sinh x * Real.sinh z)) e =
      (-Real.sinh e) /
        (Real.sinh x * Real.sinh z) :=
    (hc.div_const _).deriv
  rw [hd, abs_div, abs_neg,
    abs_of_pos he, abs_of_pos (mul_pos hx hz)]
  field_simp [ne_of_gt hx, ne_of_gt hz] <;> ring

#print axioms angular_density

end Chronos.RapidityGeometry
