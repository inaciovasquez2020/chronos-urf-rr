import Chronos.Frontier.PrizcarbonProposedRadialWeightedChiFirstVariation

namespace Chronos.Frontier

noncomputable section

/--
`C¹` regularity data for the three unrestricted radial functions stored in a
Regge–Wheeler odd-parity radial jet.

Continuity, differentiability, and continuity of the directional Fréchet
derivative are derived from these stronger component hypotheses.
-/
structure ProposedPrizcarbonRadialJetAnalyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet) : Prop where
  firstContDiffOne :
    ContDiff ℝ 1 rawState.1
  secondContDiffOne :
    ContDiff ℝ 1 rawState.2.1
  thirdContDiffOne :
    ContDiff ℝ 1 rawState.2.2

theorem proposedPrizcarbon_masterField_contDiffOne_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    ContDiff ℝ 1
      (reggeWheelerOddParityMasterField rawState) := by
  change ContDiff ℝ 1
    (fun radius : ℝ =>
      rawState.1 radius
        - (1 / 2 : ℝ) * rawState.2.1 radius
        + rawState.2.2 radius)

  have hHalfSecond :
      ContDiff ℝ 1
        (fun radius : ℝ =>
          (1 / 2 : ℝ) * rawState.2.1 radius) :=
    contDiff_const.mul hAnalytic.secondContDiffOne

  exact
    (hAnalytic.firstContDiffOne.sub hHalfSecond).add
      hAnalytic.thirdContDiffOne

theorem proposedPrizcarbon_masterField_continuous_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
      (reggeWheelerOddParityMasterField rawState) :=
  (proposedPrizcarbon_masterField_contDiffOne_of_analyticCarrier
    rawState hAnalytic).continuous

theorem proposedPrizcarbon_masterField_differentiable_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Differentiable ℝ
      (reggeWheelerOddParityMasterField rawState) :=
  (proposedPrizcarbon_masterField_contDiffOne_of_analyticCarrier
    rawState hAnalytic).differentiable (by norm_num)

theorem proposedPrizcarbon_radialWeightedChi_contDiffOne_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    ContDiff ℝ 1
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) := by
  unfold proposedPrizcarbonRadialWeightedChiCandidate
  exact
    contDiff_id.mul
      (proposedPrizcarbon_masterField_contDiffOne_of_analyticCarrier
        rawState hAnalytic)

theorem proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) :=
  (proposedPrizcarbon_radialWeightedChi_contDiffOne_of_analyticCarrier
    rawState hAnalytic).continuous

theorem proposedPrizcarbon_radialWeightedChi_differentiable_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Differentiable ℝ
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) :=
  (proposedPrizcarbon_radialWeightedChi_contDiffOne_of_analyticCarrier
    rawState hAnalytic).differentiable (by norm_num)

/--
`C¹` regularity of the three radial-jet components implies continuity of the
directional Fréchet derivative of the radial-weighted chi profile.
-/
theorem proposedPrizcarbon_radialWeightedChiDerivative_continuous_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
      (fun x : ℝ =>
        (fderiv ℝ
            (proposedPrizcarbonRadialWeightedChiCandidate
              rawState) x) 1) := by
  have hChiContDiff :
      ContDiff ℝ 1
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState) :=
    proposedPrizcarbon_radialWeightedChi_contDiffOne_of_analyticCarrier
      rawState hAnalytic

  exact
    (hChiContDiff.continuous_fderiv
      (by norm_num)).clm_apply continuous_const

theorem proposedPrizcarbon_radialWeightedChi_regular_for_variationSupport
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation : ℝ → ℝ)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState) ∧
      ∀ radius ∈ tsupport variation,
        DifferentiableAt ℝ
          (proposedPrizcarbonRadialWeightedChiCandidate
            rawState)
          radius := by
  constructor
  · exact
      proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
        rawState hAnalytic
  · intro radius _
    exact
      proposedPrizcarbon_radialWeightedChi_differentiable_of_analyticCarrier
        rawState hAnalytic radius

/--
The radial-jet analytic carrier discharges continuity and differentiability of
the radial-weighted chi profile in the compact-support first-variation theorem.
-/
theorem proposedPrizcarbon_radialWeightedChi_firstVariation_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation potential : ℝ → ℝ)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState)
    (hVariationContinuous : Continuous variation)
    (hPotentialContinuous : Continuous potential)
    (hVariationCompact : HasCompactSupport variation)
    (hDerivativeChiTimesVariation :
      MeasureTheory.Integrable
        (fun x : ℝ =>
          (fderiv ℝ
              (proposedPrizcarbonRadialWeightedChiCandidate
                rawState) x) 1 *
            variation x)
        MeasureTheory.volume)
    (hChiTimesDerivativeVariation :
      MeasureTheory.Integrable
        (fun x : ℝ =>
          proposedPrizcarbonRadialWeightedChiCandidate
              rawState x *
            (fderiv ℝ variation x) 1)
        MeasureTheory.volume)
    (hVariationDifferentiable :
      ∀ x ∈
          tsupport
            (proposedPrizcarbonRadialWeightedChiCandidate
              rawState),
        DifferentiableAt ℝ variation x) :
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
    proposedPrizcarbon_radialWeightedChi_firstVariation_eq_residualPairing
      (rawState := rawState)
      (variation := variation)
      (potential := potential)
      (hChiContinuous :=
        proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
          rawState hAnalytic)
      (hVariationContinuous := hVariationContinuous)
      (hPotentialContinuous := hPotentialContinuous)
      (hVariationCompact := hVariationCompact)
      (hDerivativeChiTimesVariation :=
        hDerivativeChiTimesVariation)
      (hChiTimesDerivativeVariation :=
        hChiTimesDerivativeVariation)
      (hChiDifferentiable := by
        intro x _
        exact
          proposedPrizcarbon_radialWeightedChi_differentiable_of_analyticCarrier
            rawState hAnalytic x)
      (hVariationDifferentiable :=
        hVariationDifferentiable)

end

end Chronos.Frontier
