import Chronos.Frontier.PrizcarbonProposedCovariantActionCarrier
import Chronos.Frontier.PrizcarbonProposedRadialProductRuleTransformation

namespace Chronos.Frontier

noncomputable section

/--
The local mass-radius coefficient appearing in the proposed scalar
Euler–Lagrange residual.
-/
def proposedPrizcarbonScalarMassRadiusCoefficient
    (r3 mass radius : ℝ) : ℝ :=
  (r3 - 8) * mass / radius ^ 3

/--
A local Euler–Lagrange jet obtained by substituting the radial-weighted
candidate chi profile and its product-rule second derivative.

The remaining residual components are set to zero because this jet is used
only to compare the scalar equation.
-/
def proposedPrizcarbonRadialWeightedScalarComparisonJet
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (mass radius : ℝ) :
    ProposedPrizcarbonEulerLagrangeJet :=
  {
    boxPseudoscalar :=
      proposedPrizcarbonRadialWeightedChiSecondDerivative
        carrier radius
    pseudoscalar :=
      proposedPrizcarbonRadialWeightedChiCandidate
        rawState radius
    arealRadius := radius
    massAspect := mass
    arealRadiusGradientSq := 0
    massDerivative := 0
    currentDivergence := 0
    multiplier := 0
    multiplierRadiusGradientDivergence := 0
    einsteinTensorComponent := 0
    stressTensorComponent := 0
  }

/--
Exact comparison of the proposed scalar Euler–Lagrange residual with the
radial-weighted master residual.

The difference consists only of the mismatch between the conditional master
potential and the proposed scalar mass-radius coefficient.
-/
theorem proposedPrizcarbon_scalarResidual_eq_negMasterResidual_addMismatch
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (r3 mass radius : ℝ) :
    proposedPrizcarbonScalarEulerLagrangeResidual
          r3
          (proposedPrizcarbonRadialWeightedScalarComparisonJet
            carrier mass radius) =
      -proposedPrizcarbonRadialWeightedMasterResidual
          carrier radius
        +
          (
            carrier.potential radius
              -
                proposedPrizcarbonScalarMassRadiusCoefficient
                  r3 mass radius
          )
          *
            proposedPrizcarbonRadialWeightedChiCandidate
              rawState radius := by
  unfold
    proposedPrizcarbonScalarEulerLagrangeResidual
    proposedPrizcarbonRadialWeightedScalarComparisonJet
    proposedPrizcarbonRadialWeightedMasterResidual
    proposedPrizcarbonScalarMassRadiusCoefficient
  ring

/--
Using the conditional master equation, the proposed scalar residual equals
the radial source `2 Psi'` plus the potential-coefficient mismatch.
-/
theorem proposedPrizcarbon_scalarResidual_eq_source_addMismatch
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (r3 mass radius : ℝ) :
    proposedPrizcarbonScalarEulerLagrangeResidual
          r3
          (proposedPrizcarbonRadialWeightedScalarComparisonJet
            carrier mass radius) =
      2 * carrier.firstDerivative radius
        +
          (
            carrier.potential radius
              -
                proposedPrizcarbonScalarMassRadiusCoefficient
                  r3 mass radius
          )
          *
            proposedPrizcarbonRadialWeightedChiCandidate
              rawState radius := by
  rw [
    proposedPrizcarbon_scalarResidual_eq_negMasterResidual_addMismatch,
    proposedPrizcarbon_radialWeightedMasterResidual_eq
  ]
  ring

/--
When the conditional master potential matches the proposed scalar
mass-radius coefficient, the scalar residual is exactly `2 Psi'`.
-/
theorem proposedPrizcarbon_scalarResidual_of_matchedCoefficient
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (r3 mass radius : ℝ)
    (hCoefficientMatch :
      carrier.potential radius =
        proposedPrizcarbonScalarMassRadiusCoefficient
          r3 mass radius) :
    proposedPrizcarbonScalarEulerLagrangeResidual
          r3
          (proposedPrizcarbonRadialWeightedScalarComparisonJet
            carrier mass radius) =
      2 * carrier.firstDerivative radius := by
  rw [
    proposedPrizcarbon_scalarResidual_eq_source_addMismatch,
    hCoefficientMatch
  ]
  ring

/--
Under exact coefficient matching, the radial-weighted candidate solves the
proposed homogeneous scalar equation at a point exactly when the conditional
master-profile derivative vanishes there.
-/
theorem proposedPrizcarbon_scalarResidual_eq_zero_iff_of_matchedCoefficient
    {rawState : ReggeWheelerOddParityRadialJet}
    (carrier :
      ProposedPrizcarbonConditionalReggeWheelerMasterEquationCarrier
        rawState)
    (r3 mass radius : ℝ)
    (hCoefficientMatch :
      carrier.potential radius =
        proposedPrizcarbonScalarMassRadiusCoefficient
          r3 mass radius) :
    proposedPrizcarbonScalarEulerLagrangeResidual
          r3
          (proposedPrizcarbonRadialWeightedScalarComparisonJet
            carrier mass radius) =
        0
      ↔
        carrier.firstDerivative radius = 0 := by
  rw [
    proposedPrizcarbon_scalarResidual_of_matchedCoefficient
      carrier r3 mass radius hCoefficientMatch
  ]
  constructor <;> intro h
  · linarith
  · rw [h]
    ring

end

end Chronos.Frontier
