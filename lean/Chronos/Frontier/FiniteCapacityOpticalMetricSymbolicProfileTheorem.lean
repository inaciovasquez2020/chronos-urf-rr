import Mathlib
import Chronos.Frontier.FiniteCapacityOpticalMetricNumericalWitness

noncomputable section

namespace Chronos
namespace Frontier

/--
Symbolic optical profile layer.

The exponential factor is represented abstractly by `expFactor`,
with the exact assumptions needed for the optical profile:

0 < eps < 1,
R > 0,
0 < expFactor <= 1.

For the concrete profile
n(r) = 1 - eps * exp(-r / R),
one supplies expFactor = exp(-r / R).

This layer proves the monotonicity/sign structure once the admissible
exponential-factor bounds are supplied.

Boundary: symbolic optical profile theorem only, not a theorem input for
gravity closure or the physical Einstein-matter flux identity.
-/
structure FiniteCapacityOpticalMetricSymbolicProfile where
  eps : ℝ
  R : ℝ
  expFactor : ℝ
  eps_pos : 0 < eps
  eps_lt_one : eps < 1
  R_pos : 0 < R
  expFactor_pos : 0 < expFactor
  expFactor_le_one : expFactor ≤ 1

namespace FiniteCapacityOpticalMetricSymbolicProfile

def opticalIndex (P : FiniteCapacityOpticalMetricSymbolicProfile) : ℝ :=
  1 - P.eps * P.expFactor

def opticalIndexDerivativeProxy (P : FiniteCapacityOpticalMetricSymbolicProfile) : ℝ :=
  (P.eps / P.R) * P.expFactor

def opticalAlphaDerivativeProxy (P : FiniteCapacityOpticalMetricSymbolicProfile) : ℝ :=
  -2 * ((P.opticalIndex ^ 3)⁻¹) * P.opticalIndexDerivativeProxy

end FiniteCapacityOpticalMetricSymbolicProfile

theorem finite_capacity_optical_metric_symbolic_index_positive
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  0 < P.opticalIndex := by
  have hmul_le : P.eps * P.expFactor ≤ P.eps * 1 := by
    exact mul_le_mul_of_nonneg_left P.expFactor_le_one (le_of_lt P.eps_pos)
  have hmul_lt_one : P.eps * P.expFactor < 1 := by
    nlinarith [hmul_le, P.eps_lt_one]
  dsimp [FiniteCapacityOpticalMetricSymbolicProfile.opticalIndex]
  nlinarith

theorem finite_capacity_optical_metric_symbolic_index_lt_one
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  P.opticalIndex < 1 := by
  have hmul_pos : 0 < P.eps * P.expFactor := by
    exact mul_pos P.eps_pos P.expFactor_pos
  dsimp [FiniteCapacityOpticalMetricSymbolicProfile.opticalIndex]
  nlinarith

theorem finite_capacity_optical_metric_symbolic_center_lower_bound
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  1 - P.eps ≤ P.opticalIndex := by
  have hmul_le : P.eps * P.expFactor ≤ P.eps * 1 := by
    exact mul_le_mul_of_nonneg_left P.expFactor_le_one (le_of_lt P.eps_pos)
  dsimp [FiniteCapacityOpticalMetricSymbolicProfile.opticalIndex]
  nlinarith

theorem finite_capacity_optical_metric_symbolic_center_lower_bound_positive
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  0 < 1 - P.eps := by
  nlinarith [P.eps_lt_one]

theorem finite_capacity_optical_metric_symbolic_index_derivative_positive
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  0 < P.opticalIndexDerivativeProxy := by
  have hdiv_pos : 0 < P.eps / P.R := by
    exact div_pos P.eps_pos P.R_pos
  have hmul_pos : 0 < (P.eps / P.R) * P.expFactor := by
    exact mul_pos hdiv_pos P.expFactor_pos
  simpa [FiniteCapacityOpticalMetricSymbolicProfile.opticalIndexDerivativeProxy] using hmul_pos

theorem finite_capacity_optical_metric_symbolic_alpha_derivative_negative
  (P : FiniteCapacityOpticalMetricSymbolicProfile) :
  P.opticalAlphaDerivativeProxy < 0 := by
  have hn_pos : 0 < P.opticalIndex :=
    finite_capacity_optical_metric_symbolic_index_positive P
  have hpow_pos : 0 < P.opticalIndex ^ 3 := by
    exact pow_pos hn_pos 3
  have hinv_pos : 0 < (P.opticalIndex ^ 3)⁻¹ := by
    exact inv_pos.mpr hpow_pos
  have hderiv_pos : 0 < P.opticalIndexDerivativeProxy :=
    finite_capacity_optical_metric_symbolic_index_derivative_positive P
  have hprod_pos : 0 < 2 * ((P.opticalIndex ^ 3)⁻¹) * P.opticalIndexDerivativeProxy := by
    exact mul_pos (mul_pos (by norm_num) hinv_pos) hderiv_pos
  dsimp [FiniteCapacityOpticalMetricSymbolicProfile.opticalAlphaDerivativeProxy]
  nlinarith

def finiteCapacityOpticalMetricSymbolicProfileWitness :
  FiniteCapacityOpticalMetricSymbolicProfile where
    eps := 1 / 2
    R := 10
    expFactor := 1 / 2
    eps_pos := by norm_num
    eps_lt_one := by norm_num
    R_pos := by norm_num
    expFactor_pos := by norm_num
    expFactor_le_one := by norm_num

example :
  0 < finiteCapacityOpticalMetricSymbolicProfileWitness.opticalIndex :=
  finite_capacity_optical_metric_symbolic_index_positive
    finiteCapacityOpticalMetricSymbolicProfileWitness

example :
  finiteCapacityOpticalMetricSymbolicProfileWitness.opticalIndex < 1 :=
  finite_capacity_optical_metric_symbolic_index_lt_one
    finiteCapacityOpticalMetricSymbolicProfileWitness

example :
  0 < finiteCapacityOpticalMetricSymbolicProfileWitness.opticalIndexDerivativeProxy :=
  finite_capacity_optical_metric_symbolic_index_derivative_positive
    finiteCapacityOpticalMetricSymbolicProfileWitness

example :
  finiteCapacityOpticalMetricSymbolicProfileWitness.opticalAlphaDerivativeProxy < 0 :=
  finite_capacity_optical_metric_symbolic_alpha_derivative_negative
    finiteCapacityOpticalMetricSymbolicProfileWitness

end Frontier
end Chronos
