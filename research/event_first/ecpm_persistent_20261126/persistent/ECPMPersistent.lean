import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

namespace Chronos.ECPM.Persistent

theorem marginal_preserved (a : ℝ) :
    1/2 + (1+a)/4 + (1-a)/4 = 1 := by
  ring

theorem joint_density (a b : ℝ) :
    1/2 + (1+a)*(1+b)/4 +
      (1-a)*(1-b)/4 = 1 + a*b/2 := by
  ring

theorem component_covariance (e k : ℝ) :
    (e*k)^2/4 + (-e*k)^2/4 -
      (e*k/4 + (-e*k)/4)^2 =
        e^2*k^2/2 := by
  ring

theorem component_covariance_pos
    (e k : ℝ) (he : 0 < e) (hk : 0 < k) :
    0 < e^2*k^2/2 := by
  positivity

theorem disjoint_pair_covariance (p d : ℝ) :
    p^2/2 + (p+d)^2/2 -
      (p/2+(p+d)/2)^2 = d^2/4 := by
  ring

theorem disjoint_pair_covariance_pos
    (e j : ℝ) (he : 0 < e) (hj : 0 < j) :
    0 < e^4*j^2/4 := by
  positivity

theorem curvature_witness
    (a t : ℝ) (ha : 0 < a) (ht : 0 < t) :
    0 < 9*a^2/(8*t^2) := by
  positivity

theorem curvature_center (a : ℝ) :
    9*a^2/(8*(1/2 : ℝ)^2) = 9*a^2/2 := by
  ring

#print axioms marginal_preserved
#print axioms joint_density
#print axioms component_covariance
#print axioms component_covariance_pos
#print axioms disjoint_pair_covariance
#print axioms disjoint_pair_covariance_pos
#print axioms curvature_witness
#print axioms curvature_center

end Chronos.ECPM.Persistent
