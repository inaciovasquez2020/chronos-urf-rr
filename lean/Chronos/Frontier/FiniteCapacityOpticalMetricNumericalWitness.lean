import Mathlib
import Chronos.Frontier.FiniteCapacityOpticalMetricDeflectionSourceMap

namespace Chronos
namespace Frontier

/--
Numerical sanity witness for the finite-capacity optical metric deflection map.

Values:

center index n0 = 1/2
outer index n1 = 3/4
center alpha alpha0 = 4
outer alpha alpha1 = 16/9

The witness checks:
0 < n0 < n1, so the refractive index is lower at the center and larger outward.
0 < alpha1 < alpha0, so alpha decreases outward.
The alpha values remain bounded by 4.

This is a numerical sanity witness only, not a theorem input.
-/
structure FiniteCapacityOpticalMetricNumericalWitness where
  centerIndex : ℚ
  outerIndex : ℚ
  centerAlpha : ℚ
  outerAlpha : ℚ
  centerIndexPositive : 0 < centerIndex
  outerIndexPositive : 0 < outerIndex
  lowerIndexAtCenter : centerIndex < outerIndex
  outerAlphaPositive : 0 < outerAlpha
  alphaDecreasesOutward : outerAlpha < centerAlpha
  centerAlphaBounded : centerAlpha ≤ 4
  outerAlphaBounded : outerAlpha ≤ 4
  sourceMapOnlyNotTheoremInput : Prop

def finiteCapacityOpticalMetricNumericalWitness :
  FiniteCapacityOpticalMetricNumericalWitness where
    centerIndex := 1 / 2
    outerIndex := 3 / 4
    centerAlpha := 4
    outerAlpha := 16 / 9
    centerIndexPositive := by norm_num
    outerIndexPositive := by norm_num
    lowerIndexAtCenter := by norm_num
    outerAlphaPositive := by norm_num
    alphaDecreasesOutward := by norm_num
    centerAlphaBounded := by norm_num
    outerAlphaBounded := by norm_num
    sourceMapOnlyNotTheoremInput := True

theorem finite_capacity_optical_metric_value_test_lower_index_at_center :
  finiteCapacityOpticalMetricNumericalWitness.centerIndex <
    finiteCapacityOpticalMetricNumericalWitness.outerIndex := by
  exact finiteCapacityOpticalMetricNumericalWitness.lowerIndexAtCenter

theorem finite_capacity_optical_metric_value_test_alpha_decreases_outward :
  finiteCapacityOpticalMetricNumericalWitness.outerAlpha <
    finiteCapacityOpticalMetricNumericalWitness.centerAlpha := by
  exact finiteCapacityOpticalMetricNumericalWitness.alphaDecreasesOutward

theorem finite_capacity_optical_metric_value_test_alpha_bounded :
  finiteCapacityOpticalMetricNumericalWitness.centerAlpha ≤ 4 ∧
    finiteCapacityOpticalMetricNumericalWitness.outerAlpha ≤ 4 := by
  exact ⟨
    finiteCapacityOpticalMetricNumericalWitness.centerAlphaBounded,
    finiteCapacityOpticalMetricNumericalWitness.outerAlphaBounded
  ⟩

theorem finite_capacity_optical_metric_value_test_boundary_closed :
  finiteCapacityOpticalMetricNumericalWitness.sourceMapOnlyNotTheoremInput := by
  trivial

end Frontier
end Chronos
