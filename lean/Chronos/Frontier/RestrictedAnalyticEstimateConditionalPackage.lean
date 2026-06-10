import Mathlib

noncomputable section

open scoped ENNReal

namespace Chronos
namespace Frontier

structure RestrictedAnalyticEstimateData where
  N : ℝ → ℝ≥0∞
  Q : ℝ → ℝ
  Qstar : ℝ
  C : ℝ≥0∞
  FluxDefect : ℝ → ℝ
  bootstrapBound : ∀ t, Q t < Qstar → N t ≤ C
  finiteC : C < ⊤
  fluxNonnegative : ∀ t, 0 ≤ FluxDefect t
  derivativeIdentity : ∀ t, deriv Q t = FluxDefect t

def RestrictedConcentrationMonotonicity
  (D : RestrictedAnalyticEstimateData) : Prop :=
  ∀ t, 0 ≤ deriv D.Q t

theorem restricted_concentration_monotonicity
  (D : RestrictedAnalyticEstimateData) :
  RestrictedConcentrationMonotonicity D := by
  intro t
  rw [D.derivativeIdentity t]
  exact D.fluxNonnegative t

def RestrictedAnalyticEstimateContinuationNormControl
  (D : RestrictedAnalyticEstimateData) : Prop :=
  ∀ t, D.Q t < D.Qstar → D.N t < ⊤

theorem restricted_continuation_norm_control
  (D : RestrictedAnalyticEstimateData) :
  RestrictedAnalyticEstimateContinuationNormControl D := by
  intro t hQ
  exact lt_of_le_of_lt (D.bootstrapBound t hQ) D.finiteC

structure RestrictedConcreteAnalyticEinsteinMatterEstimatePackage where
  data : RestrictedAnalyticEstimateData
  concentrationMonotonicity : RestrictedConcentrationMonotonicity data
  continuationNormControl : RestrictedAnalyticEstimateContinuationNormControl data

def concrete_analytic_einstein_matter_estimate_package_from_flux_and_bootstrap
  (D : RestrictedAnalyticEstimateData) :
  RestrictedConcreteAnalyticEinsteinMatterEstimatePackage where
    data := D
    concentrationMonotonicity := restricted_concentration_monotonicity D
    continuationNormControl := restricted_continuation_norm_control D

def numericalRestrictedAnalyticEstimateData :
  RestrictedAnalyticEstimateData where
    N := fun _ => (5 : ℝ≥0∞)
    Q := fun _ => (0 : ℝ)
    Qstar := 1
    C := (10 : ℝ≥0∞)
    FluxDefect := fun _ => 0
    bootstrapBound := by
      intro t hQ
      norm_num
    finiteC := by
      norm_num
    fluxNonnegative := by
      intro t
      norm_num
    derivativeIdentity := by
      intro t
      simp

def numericalConcreteAnalyticEinsteinMatterEstimatePackage :
  RestrictedConcreteAnalyticEinsteinMatterEstimatePackage :=
  concrete_analytic_einstein_matter_estimate_package_from_flux_and_bootstrap
    numericalRestrictedAnalyticEstimateData

example :
  RestrictedConcentrationMonotonicity numericalRestrictedAnalyticEstimateData :=
  numericalConcreteAnalyticEinsteinMatterEstimatePackage.concentrationMonotonicity

example :
  RestrictedAnalyticEstimateContinuationNormControl numericalRestrictedAnalyticEstimateData :=
  numericalConcreteAnalyticEinsteinMatterEstimatePackage.continuationNormControl

example :
  numericalRestrictedAnalyticEstimateData.N 0 < ⊤ := by
  exact restricted_continuation_norm_control
    numericalRestrictedAnalyticEstimateData
    0
    (by norm_num [numericalRestrictedAnalyticEstimateData])

end Frontier
end Chronos
