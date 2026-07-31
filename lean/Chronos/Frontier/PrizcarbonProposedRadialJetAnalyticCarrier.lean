import Chronos.Frontier.PrizcarbonProposedRadialWeightedChiFirstVariation

namespace Chronos.Frontier

noncomputable section

/--
Analytic regularity data for the three unrestricted radial functions stored in
a Regge–Wheeler odd-parity radial jet.

The underlying radial-jet type stores no continuity or differentiability
properties, so these hypotheses are carried separately.
-/
structure ProposedPrizcarbonRadialJetAnalyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet) : Prop where
  firstContinuous : Continuous rawState.1
  secondContinuous : Continuous rawState.2.1
  thirdContinuous : Continuous rawState.2.2
  firstDifferentiable : Differentiable ℝ rawState.1
  secondDifferentiable : Differentiable ℝ rawState.2.1
  thirdDifferentiable : Differentiable ℝ rawState.2.2

theorem proposedPrizcarbon_masterField_continuous_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
      (reggeWheelerOddParityMasterField rawState) := by
  change Continuous
    (fun radius : ℝ =>
      rawState.1 radius
        - (1 / 2 : ℝ) * rawState.2.1 radius
        + rawState.2.2 radius)

  have hHalfSecond :
      Continuous
        (fun radius : ℝ =>
          (1 / 2 : ℝ) * rawState.2.1 radius) :=
    continuous_const.mul hAnalytic.secondContinuous

  exact
    (hAnalytic.firstContinuous.sub hHalfSecond).add
      hAnalytic.thirdContinuous

theorem proposedPrizcarbon_masterField_differentiable_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Differentiable ℝ
      (reggeWheelerOddParityMasterField rawState) := by
  change Differentiable ℝ
    (fun radius : ℝ =>
      rawState.1 radius
        - (1 / 2 : ℝ) * rawState.2.1 radius
        + rawState.2.2 radius)

  have hHalfSecond :
      Differentiable ℝ
        (fun radius : ℝ =>
          (1 / 2 : ℝ) * rawState.2.1 radius) :=
    (differentiable_const (c := (1 / 2 : ℝ))).mul
      hAnalytic.secondDifferentiable

  exact
    (hAnalytic.firstDifferentiable.sub hHalfSecond).add
      hAnalytic.thirdDifferentiable

theorem proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Continuous
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) := by
  have hMaster :
      Continuous
        (reggeWheelerOddParityMasterField rawState) :=
    proposedPrizcarbon_masterField_continuous_of_analyticCarrier
      rawState hAnalytic

  unfold proposedPrizcarbonRadialWeightedChiCandidate
  exact continuous_id.mul hMaster

theorem proposedPrizcarbon_radialWeightedChi_differentiable_of_analyticCarrier
    (rawState : ReggeWheelerOddParityRadialJet)
    (hAnalytic :
      ProposedPrizcarbonRadialJetAnalyticCarrier rawState) :
    Differentiable ℝ
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState) := by
  have hMaster :
      Differentiable ℝ
        (reggeWheelerOddParityMasterField rawState) :=
    proposedPrizcarbon_masterField_differentiable_of_analyticCarrier
      rawState hAnalytic

  unfold proposedPrizcarbonRadialWeightedChiCandidate
  exact differentiable_id.mul hMaster

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

end

end Chronos.Frontier

namespace Chronos.Frontier

noncomputable section

/--
The radial-jet analytic carrier discharges the continuity and
differentiability hypotheses for the radial-weighted chi profile.

Derivative-product integrability and regularity of the compactly supported
test variation remain explicit assumptions.
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
  have hChiContinuous :
      Continuous
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState) :=
    proposedPrizcarbon_radialWeightedChi_continuous_of_analyticCarrier
      rawState hAnalytic

  have hChiDifferentiable :
      Differentiable ℝ
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState) :=
    proposedPrizcarbon_radialWeightedChi_differentiable_of_analyticCarrier
      rawState hAnalytic

  exact
    proposedPrizcarbon_radialWeightedChi_firstVariation_eq_residualPairing
      (rawState := rawState)
      (variation := variation)
      (potential := potential)
      (hChiContinuous := hChiContinuous)
      (hVariationContinuous := hVariationContinuous)
      (hPotentialContinuous := hPotentialContinuous)
      (hVariationCompact := hVariationCompact)
      (hDerivativeChiTimesVariation :=
        hDerivativeChiTimesVariation)
      (hChiTimesDerivativeVariation :=
        hChiTimesDerivativeVariation)
      (hChiDifferentiable := by
        intro x _
        exact hChiDifferentiable x)
      (hVariationDifferentiable :=
        hVariationDifferentiable)

end

end Chronos.Frontier
