import Mathlib.Data.Real.Basic

namespace Chronos.Frontier

structure AMSIsotopeCharacterizationSurface where
  C12_fraction : ℝ
  C13_fraction : ℝ
  C14_fraction : ℝ
  fraction_sum : C12_fraction + C13_fraction + C14_fraction = 1

structure CarbonAllotropeIdentitySurface where
  Sample : Type
  diamond_sample : Sample
  graphite_sample : Sample

structure EotvosWEPBoundInputSurface where
  eta_bound : ℝ
  eta_bound_nonnegative : 0 ≤ eta_bound

structure CarbonStructuralResidualInputSurface where
  eta_structure : ℝ

def CarbonStructuralGravityProven : Prop := False

theorem carbon_structural_gravity_not_proven :
    ¬ CarbonStructuralGravityProven := by
  intro h
  exact h

structure PositiveAccelerationInterval where
  x_minus : ℝ
  x_plus  : ℝ
  y_minus : ℝ
  y_plus  : ℝ
  hx_minus_pos : 0 < x_minus
  hy_minus_pos : 0 < y_minus
  hx_order : x_minus ≤ x_plus
  hy_order : y_minus ≤ y_plus

theorem eta_denominator_min_pos (I : PositiveAccelerationInterval) :
    0 < I.x_minus + I.y_plus := by
  exact add_pos_of_pos_of_nonneg I.hx_minus_pos
    (le_trans (le_of_lt I.hy_minus_pos) I.hy_order)

theorem eta_denominator_max_pos (I : PositiveAccelerationInterval) :
    0 < I.x_plus + I.y_minus := by
  exact add_pos_of_nonneg_of_pos
    (le_trans (le_of_lt I.hx_minus_pos) I.hx_order)
    I.hy_minus_pos

noncomputable def etaMin (I : PositiveAccelerationInterval) : ℝ :=
  2 * (I.x_minus - I.y_plus) / (I.x_minus + I.y_plus)

noncomputable def etaMax (I : PositiveAccelerationInterval) : ℝ :=
  2 * (I.x_plus - I.y_minus) / (I.x_plus + I.y_minus)

structure CDTSampleSpecificationSurface where
  Sample : Type
  sample_A : Sample
  sample_B : Sample
  mass_matched : Prop
  isotope_matched : Prop
  purity_matched : Prop
  geometry_matched : Prop
  center_of_mass_matched : Prop
  charge_neutralized : Prop
  magnetic_response_bounded : Prop

structure CDTMeasurementProtocolSurface where
  Trial : Type
  acceleration_A : Trial → ℝ
  acceleration_B : Trial → ℝ
  eta_CDT : Trial → ℝ
  eta_def :
    ∀ t : Trial,
      eta_CDT t =
        2 * (acceleration_A t - acceleration_B t) /
          (acceleration_A t + acceleration_B t)

structure CDTUncertaintyBudgetSurface where
  delta_eta_stat : ℝ
  delta_eta_sys : ℝ
  delta_eta_env : ℝ
  delta_eta_calibration : ℝ
  delta_eta_disturbance : ℝ
  delta_eta_total : ℝ
  h_total_nonneg : 0 ≤ delta_eta_total

structure CDTDecisionRuleSurface where
  eta_observed : ℝ
  delta_eta_total : ℝ
  k : ℝ
  h_delta_nonneg : 0 ≤ delta_eta_total
  h_k_pos : 0 < k
  detected : Prop
  h_detected_iff : detected ↔ |eta_observed| > k * delta_eta_total

theorem cdt_detected_eta_nonzero (S : CDTDecisionRuleSurface)
    (h : S.detected) : S.eta_observed ≠ 0 := by
  intro hzero
  have hdet : |S.eta_observed| > S.k * S.delta_eta_total :=
    S.h_detected_iff.mp h
  rw [hzero, abs_zero] at hdet
  have hk_nonneg : 0 ≤ S.k := le_of_lt S.h_k_pos
  have hprod_nonneg : 0 ≤ S.k * S.delta_eta_total :=
    mul_nonneg hk_nonneg S.h_delta_nonneg
  exact not_lt_of_ge hprod_nonneg hdet

structure CDTNullControlPairSurface where
  ControlSample : Type
  control_A : ControlSample
  control_B : ControlSample
  same_material_pair : Prop
  null_expected : Prop

structure CDTReplicationCriterionInputSurface where
  independent_labs : Prop
  same_sign_across_labs : Prop
  magnitude_agrees_within_uncertainty : Prop
  survives_sample_swapping : Prop
  survives_blinding : Prop
  survives_location_change : Prop
  survives_instrument_change : Prop
  null_controls_absent : Prop

def CDTCarbonStructuralGravityCausalClaim : Prop := False

theorem cdt_rejects_causal_overclaim :
    ¬ CDTCarbonStructuralGravityCausalClaim := by
  intro h
  exact h

end Chronos.Frontier
