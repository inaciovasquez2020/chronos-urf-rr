import Chronos.Frontier.PrizcarbonProposedFirstVariationOperator
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts

namespace Chronos.Frontier

noncomputable section

def proposedPrizcarbonScalarFirstVariationIntegrand
    (field variation potential : ℝ → ℝ)
    (x : ℝ) : ℝ :=
  field x * (fderiv ℝ variation x) 1
    + potential x * field x * variation x

def proposedPrizcarbonScalarEulerLagrangePairingIntegrand
    (field variation potential : ℝ → ℝ)
    (x : ℝ) : ℝ :=
  (-(fderiv ℝ field x) 1 + potential x * field x) *
    variation x

theorem proposedPrizcarbon_compactSupportFieldVariation_integrable
    (field variation : ℝ → ℝ)
    (hFieldContinuous : Continuous field)
    (hVariationContinuous : Continuous variation)
    (hVariationCompact : HasCompactSupport variation) :
    MeasureTheory.Integrable
      (fun x : ℝ => field x * variation x)
      MeasureTheory.volume := by
  have hContinuous :
      Continuous (fun x : ℝ => field x * variation x) :=
    hFieldContinuous.mul hVariationContinuous
  have hCompact :
      HasCompactSupport (fun x : ℝ => field x * variation x) :=
    hVariationCompact.mul_left
  exact hContinuous.integrable_of_hasCompactSupport hCompact

theorem proposedPrizcarbon_compactSupportPotentialVariation_integrable
    (field variation potential : ℝ → ℝ)
    (hFieldContinuous : Continuous field)
    (hVariationContinuous : Continuous variation)
    (hPotentialContinuous : Continuous potential)
    (hVariationCompact : HasCompactSupport variation) :
    MeasureTheory.Integrable
      (fun x : ℝ => potential x * field x * variation x)
      MeasureTheory.volume := by
  have hContinuous :
      Continuous
        (fun x : ℝ => potential x * field x * variation x) :=
    (hPotentialContinuous.mul hFieldContinuous).mul
      hVariationContinuous
  have hCompact :
      HasCompactSupport
        (fun x : ℝ => potential x * field x * variation x) :=
    hVariationCompact.mul_left
  exact hContinuous.integrable_of_hasCompactSupport hCompact

theorem proposedPrizcarbon_scalarFirstVariation_eq_residualPairing
    (field variation potential : ℝ → ℝ)
    (hFieldContinuous : Continuous field)
    (hVariationContinuous : Continuous variation)
    (hPotentialContinuous : Continuous potential)
    (hVariationCompact : HasCompactSupport variation)
    (hDerivativeFieldTimesVariation :
      MeasureTheory.Integrable
        (fun x : ℝ =>
          (fderiv ℝ field x) 1 * variation x)
        MeasureTheory.volume)
    (hFieldTimesDerivativeVariation :
      MeasureTheory.Integrable
        (fun x : ℝ =>
          field x * (fderiv ℝ variation x) 1)
        MeasureTheory.volume)
    (hFieldDifferentiable :
      ∀ x ∈ tsupport variation,
        DifferentiableAt ℝ field x)
    (hVariationDifferentiable :
      ∀ x ∈ tsupport field,
        DifferentiableAt ℝ variation x) :
    (∫ x : ℝ,
        proposedPrizcarbonScalarFirstVariationIntegrand
          field variation potential x) =
      ∫ x : ℝ,
        proposedPrizcarbonScalarEulerLagrangePairingIntegrand
          field variation potential x := by
  have hFieldTimesVariation :
      MeasureTheory.Integrable
        (fun x : ℝ => field x * variation x)
        MeasureTheory.volume :=
    proposedPrizcarbon_compactSupportFieldVariation_integrable
      field variation
      hFieldContinuous
      hVariationContinuous
      hVariationCompact

  have hPotentialTerm :
      MeasureTheory.Integrable
        (fun x : ℝ =>
          potential x * field x * variation x)
        MeasureTheory.volume :=
    proposedPrizcarbon_compactSupportPotentialVariation_integrable
      field variation potential
      hFieldContinuous
      hVariationContinuous
      hPotentialContinuous
      hVariationCompact

  have hIntegrationByParts :
      (∫ x : ℝ,
          field x * (fderiv ℝ variation x) 1) =
        -∫ x : ℝ,
          (fderiv ℝ field x) 1 * variation x :=
    integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable
      (μ := MeasureTheory.volume)
      (v := (1 : ℝ))
      hDerivativeFieldTimesVariation
      hFieldTimesDerivativeVariation
      hFieldTimesVariation
      hFieldDifferentiable
      hVariationDifferentiable

  unfold proposedPrizcarbonScalarFirstVariationIntegrand
    proposedPrizcarbonScalarEulerLagrangePairingIntegrand

  calc
    (∫ x : ℝ,
        field x * (fderiv ℝ variation x) 1
          + potential x * field x * variation x) =
        (∫ x : ℝ,
          field x * (fderiv ℝ variation x) 1)
          + ∫ x : ℝ,
            potential x * field x * variation x := by
      simpa only [Pi.add_apply] using
        MeasureTheory.integral_add
          hFieldTimesDerivativeVariation
          hPotentialTerm
    _ =
        (-∫ x : ℝ,
          (fderiv ℝ field x) 1 * variation x)
          + ∫ x : ℝ,
            potential x * field x * variation x := by
      rw [hIntegrationByParts]
    _ =
        (∫ x : ℝ,
          -((fderiv ℝ field x) 1 * variation x))
          + ∫ x : ℝ,
            potential x * field x * variation x := by
      rw [← MeasureTheory.integral_neg]
    _ =
        ∫ x : ℝ,
          -((fderiv ℝ field x) 1 * variation x)
            + potential x * field x * variation x := by
      symm
      simpa only [Pi.add_apply, Pi.neg_apply] using
        MeasureTheory.integral_add
          hDerivativeFieldTimesVariation.neg
          hPotentialTerm
    _ =
        ∫ x : ℝ,
          (-(fderiv ℝ field x) 1
              + potential x * field x) *
            variation x := by
      apply MeasureTheory.integral_congr_ae
      filter_upwards [] with x
      ring

end

end Chronos.Frontier
