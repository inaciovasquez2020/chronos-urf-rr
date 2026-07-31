import Chronos.Frontier.PrizcarbonProposedRadialJetAnalyticCarrier

namespace Chronos.Frontier

noncomputable section

/--
`C¹`, compact-support data for the scalar test variation.

Continuity, differentiability, derivative continuity, and derivative compact
support are derived from the two stored fields.
-/
structure ProposedPrizcarbonScalarVariationAnalyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ) : Prop where
  variationCompact :
    HasCompactSupport variation
  variationContDiffOne :
    ContDiff ℝ 1 variation

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

theorem proposedPrizcarbon_variation_continuous_of_differentiable
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    Continuous variation :=
  hVariation.variationContDiffOne.continuous

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
  exact
    hVariation.variationContDiffOne.differentiable
      (by norm_num) x

/--
`C¹` regularity of the test variation implies continuity of its directional
Fréchet derivative.
-/
theorem proposedPrizcarbon_variationDerivative_continuous_of_contDiffOne
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hVariation :
      ProposedPrizcarbonScalarVariationAnalyticCarrier
        rawState variation) :
    Continuous
      (fun x : ℝ =>
        (fderiv ℝ variation x) 1) := by
  exact
    (hVariation.variationContDiffOne.continuous_fderiv
      (by norm_num)).clm_apply continuous_const

theorem proposedPrizcarbon_derivativeChiTimesVariation_integrable
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hRawAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState)
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
    (proposedPrizcarbon_radialWeightedChiDerivative_continuous_of_analyticCarrier
      rawState hRawAnalytic).mul
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
  have hContinuous :
      Continuous
        (fun x : ℝ =>
          proposedPrizcarbonRadialWeightedChiCandidate
              rawState x *
            (fderiv ℝ variation x) 1) :=
    (proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
      rawState hRawAnalytic).mul
        (proposedPrizcarbon_variationDerivative_continuous_of_contDiffOne
          rawState variation hVariation)

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
          rawState variation
          hRawAnalytic hVariation)
      (hChiTimesDerivativeVariation :=
        proposedPrizcarbon_chiTimesDerivativeVariation_integrable
          rawState variation
          hRawAnalytic hVariation)
      (hVariationDifferentiable :=
        proposedPrizcarbon_variation_differentiableOnChiSupport
          rawState variation hVariation)

end

end Chronos.Frontier
