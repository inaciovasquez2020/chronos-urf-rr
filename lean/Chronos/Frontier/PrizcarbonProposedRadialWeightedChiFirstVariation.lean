import Chronos.Frontier.PrizcarbonProposedMetricToChiBridgeCarrier

namespace Chronos.Frontier

noncomputable section

/--
The proved compact-support scalar first-variation identity specialized to the
radial-weighted candidate chi profile.

All continuity, differentiability, compact-support, and integrability
conditions remain explicit. This theorem does not derive those analytic
conditions from the metric radial jet, and it does not derive the radial
weighting ansatz from the covariant action.
-/
theorem proposedPrizcarbon_radialWeightedChi_firstVariation_eq_residualPairing
    (rawState : ReggeWheelerOddParityRadialJet)
    (variation potential : ℝ → ℝ)
    (hChiContinuous :
      Continuous
        (proposedPrizcarbonRadialWeightedChiCandidate
          rawState))
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
    (hChiDifferentiable :
      ∀ x ∈ tsupport variation,
        DifferentiableAt ℝ
          (proposedPrizcarbonRadialWeightedChiCandidate
            rawState) x)
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
    proposedPrizcarbon_scalarFirstVariation_eq_residualPairing
      (field :=
        proposedPrizcarbonRadialWeightedChiCandidate
          rawState)
      (variation := variation)
      (potential := potential)
      (hFieldContinuous := hChiContinuous)
      (hVariationContinuous := hVariationContinuous)
      (hPotentialContinuous := hPotentialContinuous)
      (hVariationCompact := hVariationCompact)
      (hDerivativeFieldTimesVariation :=
        hDerivativeChiTimesVariation)
      (hFieldTimesDerivativeVariation :=
        hChiTimesDerivativeVariation)
      (hFieldDifferentiable := hChiDifferentiable)
      (hVariationDifferentiable :=
        hVariationDifferentiable)

end

end Chronos.Frontier
