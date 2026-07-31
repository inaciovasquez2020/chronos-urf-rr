import Chronos.Frontier.PrizcarbonProposedRadialJetAnalyticCarrier

namespace Chronos.Frontier

noncomputable section

/--
Regularity and compact-support data sufficient to derive both
derivative-product integrability obligations in the scalar first variation.

Compact support of the directional Fréchet derivative is derived from compact
support of the test variation using Mathlib's
`HasCompactSupport.fderiv_apply`.
-/
structure ProposedPrizcarbonScalarVariationAnalyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ) : Prop where
  variationCompact :
    HasCompactSupport variation
  chiDerivativeContinuous :
    Continuous
      (fun x : ℝ =>
        (fderiv ℝ
            (proposedPrizcarbonRadialWeightedChiCandidate
              rawState) x) 1)
  variationDerivativeContinuous :
    Continuous
      (fun x : ℝ =>
        (fderiv ℝ variation x) 1)
  variationDifferentiable :
    Differentiable ℝ variation

/--
Compact support of the test variation implies compact support of its
directional Fréchet derivative.
-/
theorem proposedPrizcarbon_variationDerivative_compact_of_compactSupport
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    HasCompactSupport
      (fun x : ℝ =>
        (fderiv ℝ variation x) 1) := by
  exact
    hVariation.variationCompact.fderiv_apply
      (𝕜 := ℝ) (1 : ℝ)

/--
Global differentiability of the test variation supplies its continuity.
-/
theorem proposedPrizcarbon_variation_continuous_of_differentiable
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    Continuous variation :=
  hVariation.variationDifferentiable.continuous

/--
Global differentiability of the test variation supplies differentiability at
every point in the support of the candidate chi profile.
-/
theorem proposedPrizcarbon_variation_differentiableOnChiSupport
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    ∀ x ∈
        tsupport
          (proposedPrizcarbonRadialWeightedChiCandidate
            rawState),
      DifferentiableAt ℝ variation x := by
  intro x _
  exact hVariation.variationDifferentiable x

/--
Continuity of the chi derivative and compact support of the test variation
imply integrability of the first derivative product.
-/
theorem proposedPrizcarbon_derivativeChiTimesVariation_integrable
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    MeasureTheory.Integrable
      (fun x : ℝ =>
        (fderiv ℝ
            (proposedPrizcarbonRadialWeightedChiCandidate
              rawState) x) 1 *
          variation x)
      MeasureTheory.volume := by
  have hContinuous :
      Continuous
        (fun x : ℝ =>
          (fderiv ℝ
              (proposedPrizcarbonRadialWeightedChiCandidate
                rawState) x) 1 *
            variation x) :=
    hVariation.chiDerivativeContinuous.mul
      (proposedPrizcarbon_variation_continuous_of_differentiable
        rawState variation hVariation)

  have hCompact :
      HasCompactSupport
        (fun x : ℝ =>
          (fderiv ℝ
              (proposedPrizcarbonRadialWeightedChiCandidate
                rawState) x) 1 *
            variation x) :=
    hVariation.variationCompact.mul_left

  exact
    hContinuous.integrable_of_hasCompactSupport hCompact

/--
Continuity of chi and of the test-variation derivative, together with compact
support of that derivative, imply integrability of the second derivative
product.
-/
theorem proposedPrizcarbon_chiTimesDerivativeVariation_integrable
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hRawAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    MeasureTheory.Integrable
      (fun x : ℝ =>
        proposedPrizcarbonRadialWeightedChiCandidate
            rawState x *
          (fderiv ℝ variation x) 1)
      MeasureTheory.volume := by
  have hChiContinuous :
      Continuous
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState) :=
    proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
      rawState hRawAnalytic

  have hContinuous :
      Continuous
        (fun x : ℝ =>
          proposedPrizcarbonRadialWeightedChiCandidate
              rawState x *
            (fderiv ℝ variation x) 1) :=
    hChiContinuous.mul
      hVariation.variationDerivativeContinuous

  have hVariationDerivativeCompact :
      HasCompactSupport
        (fun x : ℝ =>
          (fderiv ℝ variation x) 1) :=
    proposedPrizcarbon_variationDerivative_compact_of_compactSupport
      rawState variation hVariation

  have hCompact :
      HasCompactSupport
        (fun x : ℝ =>
          proposedPrizcarbonRadialWeightedChiCandidate
              rawState x *
            (fderiv ℝ variation x) 1) :=
    hVariationDerivativeCompact.mul_left

  exact
    hContinuous.integrable_of_hasCompactSupport hCompact

/--
The two derivative-product integrability assumptions are discharged by the
radial-jet and scalar-variation analytic carriers.
-/
theorem proposedPrizcarbon_radialWeightedChi_firstVariation_of_variationCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation potential : ℝ → ℝ)
    (hRawAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation)
    (hPotentialContinuous : Continuous potential) :
    (∫ x : ℝ,
        proposedPrizcarbonScalarFirstVariationIntegrand
          (proposedPrizcarbonRadialWeightedChiCandidate
            rawState)
          variation potential x) =
      ∫ x : ℝ,
        proposedPrizcarbonScalarEulerLagrangePairingIntegrand
          (proposedPrizcarbonRadialWeightedChiCandidate
            rawState)
          variation potential x := by
  exact
    proposedPrizcarbon_radialWeightedChi_firstVariation_of_analyticCarrier
      (rawState := rawState)
      (variation := variation)
      (potential := potential)
      (hAnalytic := hRawAnalytic)
      (hVariationContinuous :=
        proposedPrizcarbon_variation_continuous_of_differentiable
          rawState variation hVariation)
      (hPotentialContinuous :=
        hPotentialContinuous)
      (hVariationCompact :=
        hVariation.variationCompact)
      (hDerivativeChiTimesVariation :=
        proposedPrizcarbon_derivativeChiTimesVariation_integrable
          rawState variation hVariation)
      (hChiTimesDerivativeVariation :=
        proposedPrizcarbon_chiTimesDerivativeVariation_integrable
          rawState variation
          hRawAnalytic hVariation)
      (hVariationDifferentiable :=
        proposedPrizcarbon_variation_differentiableOnChiSupport
          rawState variation hVariation)

end

end Chronos.Frontier
