import Chronos.Frontier.PrizcarbonProposedMetricToChiBridgeCarrier

namespace Chronos.Frontier

noncomputable section

/--
A conditional differential-equation carrier for the gauge-invariant
Regge–Wheeler odd-parity master profile.

The carrier does not assert that the current radial jet satisfies a physical
Regge–Wheeler equation. It records the derivative data, a potential, and the
homogeneous equation needed to derive the radial product transformation.
-/
structure ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
    (rawState : ReggeWheelerOddParityRadialJet) where
  firstDerivative : ℝ → ℝ
  secondDerivative : ℝ → ℝ
  potential : ℝ → ℝ
  masterHasDerivAt :
    ∀ radius : ℝ,
      HasDerivAt
        (reggeWheelerOddParityMasterField rawState)
        (firstDerivative radius)
        radius
  firstDerivativeHasDerivAt :
    ∀ radius : ℝ,
      HasDerivAt
        firstDerivative
        (secondDerivative radius)
        radius
  masterEquation :
    ∀ radius : ℝ,
      -secondDerivative radius
          + potential radius *
            reggeWheelerOddParityMasterField
              rawState radius =
        0

/--
Candidate first derivative of `chi(radius) = radius * Psi(radius)`.
-/
def proposedPrizcarbonRadialWeightedChiFirstDerivative
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) : ℝ :=
  reggeWheelerOddParityMasterField rawState radius
    + radius * carrier.firstDerivative radius

/--
Candidate second derivative of `chi(radius) = radius * Psi(radius)`.
-/
def proposedPrizcarbonRadialWeightedChiSecondDerivative
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) : ℝ :=
  2 * carrier.firstDerivative radius
    + radius * carrier.secondDerivative radius

theorem proposedPrizcarbon_radialWeightedChi_hasDerivAt
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) :
    HasDerivAt
      (proposedPrizcarbonRadialWeightedChiCandidate
        rawState)
      (proposedPrizcarbonRadialWeightedChiFirstDerivative
        carrier radius)
      radius := by
  simpa [
    proposedPrizcarbonRadialWeightedChiCandidate,
    proposedPrizcarbonRadialWeightedChiFirstDerivative
  ] using
    (hasDerivAt_id radius).mul
      (carrier.masterHasDerivAt radius)

theorem proposedPrizcarbon_radialWeightedChiFirstDerivative_hasDerivAt
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) :
    HasDerivAt
      (proposedPrizcarbonRadialWeightedChiFirstDerivative
        carrier)
      (proposedPrizcarbonRadialWeightedChiSecondDerivative
        carrier radius)
      radius := by
  simpa [
    proposedPrizcarbonRadialWeightedChiFirstDerivative,
    proposedPrizcarbonRadialWeightedChiSecondDerivative,
    two_mul,
    add_assoc
  ] using
    (carrier.masterHasDerivAt radius).add
      (
        (hasDerivAt_id radius).mul
          (carrier.firstDerivativeHasDerivAt radius)
      )

/--
Residual obtained by applying the carrier's homogeneous master operator to
the radial-weighted profile.
-/
def proposedPrizcarbonRadialWeightedMasterResidual
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) : ℝ :=
  -proposedPrizcarbonRadialWeightedChiSecondDerivative
      carrier radius
    + carrier.potential radius *
        proposedPrizcarbonRadialWeightedChiCandidate
          rawState radius

/--
Exact radial product-rule transformation:

if `Psi` satisfies `-Psi'' + V Psi = 0`, then `chi = radius * Psi`
satisfies

`-chi'' + V chi = -2 Psi'`.

Thus radial weighting does not generally preserve the same homogeneous
equation.
-/
theorem proposedPrizcarbon_radialWeightedMasterResidual_eq
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) :
    proposedPrizcarbonRadialWeightedMasterResidual
        carrier radius =
      -2 * carrier.firstDerivative radius := by
  unfold
    proposedPrizcarbonRadialWeightedMasterResidual
    proposedPrizcarbonRadialWeightedChiSecondDerivative
    proposedPrizcarbonRadialWeightedChiCandidate

  calc
    -(2 * carrier.firstDerivative radius
          + radius * carrier.secondDerivative radius)
        + carrier.potential radius *
            (radius *
              reggeWheelerOddParityMasterField
                rawState radius) =
      -2 * carrier.firstDerivative radius
        + radius *
            (
              -carrier.secondDerivative radius
                + carrier.potential radius *
                    reggeWheelerOddParityMasterField
                      rawState radius
            ) := by
              ring
    _ = -2 * carrier.firstDerivative radius := by
      rw [carrier.masterEquation radius]
      ring

/--
The radial-weighted profile satisfies the same homogeneous master equation at
a point exactly when the stored first derivative of the master profile
vanishes there.
-/
theorem proposedPrizcarbon_radialWeightedMasterResidual_eq_zero_iff
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (radius : ℝ) :
    proposedPrizcarbonRadialWeightedMasterResidual
          carrier radius =
        0 ↔
      carrier.firstDerivative radius = 0 := by
  rw [
    proposedPrizcarbon_radialWeightedMasterResidual_eq
      carrier radius
  ]
  constructor <;> intro h
  · linarith
  · rw [h]
    ring

end

end Chronos.Frontier
