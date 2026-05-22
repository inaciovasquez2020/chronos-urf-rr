import Mathlib

namespace Chronos.Frontier

/-!
# WEC pointwise positivity for nonnegative scalar potential

This module proves only algebraic pointwise positivity of scalar-field
energy density when the spatial gradient norm square and potential value
are nonnegative.

It does not prove time evolution, continuation, collapse, trapped-surface
formation, cosmic censorship, the hoop conjecture, or any unrestricted
gravity theorem.
-/

noncomputable section

def scalarFieldEnergyDensity
    (pi gradSq potentialValue : ℝ) : ℝ :=
  (1 / 2 : ℝ) * pi ^ 2 + (1 / 2 : ℝ) * gradSq + potentialValue

def ScalarFieldPointwiseWEC
    (pi gradSq potentialValue : ℝ) : Prop :=
  0 ≤ scalarFieldEnergyDensity pi gradSq potentialValue

theorem wec_pointwise_positivity_for_nonnegative_scalar_potential
    (pi gradSq potentialValue : ℝ)
    (h_gradSq_nonneg : 0 ≤ gradSq)
    (h_potential_nonneg : 0 ≤ potentialValue) :
    ScalarFieldPointwiseWEC pi gradSq potentialValue := by
  unfold ScalarFieldPointwiseWEC scalarFieldEnergyDensity
  have hpi : 0 ≤ (1 / 2 : ℝ) * pi ^ 2 := by
    exact mul_nonneg (by norm_num) (sq_nonneg pi)
  have hgrad : 0 ≤ (1 / 2 : ℝ) * gradSq := by
    exact mul_nonneg (by norm_num) h_gradSq_nonneg
  linarith

theorem scalarFieldEnergyDensity_nonneg
    (pi gradSq potentialValue : ℝ)
    (h_gradSq_nonneg : 0 ≤ gradSq)
    (h_potential_nonneg : 0 ≤ potentialValue) :
    0 ≤ scalarFieldEnergyDensity pi gradSq potentialValue := by
  exact wec_pointwise_positivity_for_nonnegative_scalar_potential
    pi gradSq potentialValue h_gradSq_nonneg h_potential_nonneg

end

end Chronos.Frontier
