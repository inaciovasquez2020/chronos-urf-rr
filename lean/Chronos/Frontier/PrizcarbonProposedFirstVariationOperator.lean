import Chronos.Frontier.PrizcarbonProposedCovariantActionCarrier

namespace Chronos.Frontier

noncomputable section

/--
Independent bulk field variations paired with the six residual components of
the proposed Prizcarbon carrier.
-/
structure ProposedPrizcarbonFieldVariation where
  scalar : ℝ
  radiusConstraint : ℝ
  massConstancy : ℝ
  mass : ℝ
  radius : ℝ
  metric : ℝ

/--
Explicit bulk first-variation operator associated with the encoded
Euler–Lagrange residual carrier.

This definition supplies a proof-bearing residual pairing. It does not yet
identify this pairing with the derivative of the spacetime action integral.
-/
def proposedPrizcarbonActionFirstVariationOperator
    (newtonCoupling r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet)
    (variation : ProposedPrizcarbonFieldVariation) : ℝ :=
  let residuals :=
    proposedPrizcarbonEulerLagrangeResiduals
      newtonCoupling r3 jet
  residuals.scalar * variation.scalar
    + residuals.radiusConstraint * variation.radiusConstraint
    + residuals.massConstancy * variation.massConstancy
    + residuals.mass * variation.mass
    + residuals.radius * variation.radius
    + residuals.metric * variation.metric

def proposedPrizcarbonScalarBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 1
    radiusConstraint := 0
    massConstancy := 0
    mass := 0
    radius := 0
    metric := 0
  }

def proposedPrizcarbonRadiusConstraintBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 0
    radiusConstraint := 1
    massConstancy := 0
    mass := 0
    radius := 0
    metric := 0
  }

def proposedPrizcarbonMassConstancyBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 0
    radiusConstraint := 0
    massConstancy := 1
    mass := 0
    radius := 0
    metric := 0
  }

def proposedPrizcarbonMassBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 0
    radiusConstraint := 0
    massConstancy := 0
    mass := 1
    radius := 0
    metric := 0
  }

def proposedPrizcarbonRadiusBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 0
    radiusConstraint := 0
    massConstancy := 0
    mass := 0
    radius := 1
    metric := 0
  }

def proposedPrizcarbonMetricBasisVariation :
    ProposedPrizcarbonFieldVariation :=
  {
    scalar := 0
    radiusConstraint := 0
    massConstancy := 0
    mass := 0
    radius := 0
    metric := 1
  }

/--
Every encoded Euler–Lagrange residual is recovered exactly by evaluating the
explicit first-variation operator on its corresponding basis variation.
-/
theorem proposedPrizcarbon_actionFirstVariation_recoversResiduals
    (newtonCoupling r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) :
    let residuals :=
      proposedPrizcarbonEulerLagrangeResiduals
        newtonCoupling r3 jet
    proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonScalarBasisVariation =
        residuals.scalar ∧
      proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonRadiusConstraintBasisVariation =
        residuals.radiusConstraint ∧
      proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonMassConstancyBasisVariation =
        residuals.massConstancy ∧
      proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonMassBasisVariation =
        residuals.mass ∧
      proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonRadiusBasisVariation =
        residuals.radius ∧
      proposedPrizcarbonActionFirstVariationOperator
          newtonCoupling r3 jet
          proposedPrizcarbonMetricBasisVariation =
        residuals.metric := by
  simp [
    proposedPrizcarbonActionFirstVariationOperator,
    proposedPrizcarbonScalarBasisVariation,
    proposedPrizcarbonRadiusConstraintBasisVariation,
    proposedPrizcarbonMassConstancyBasisVariation,
    proposedPrizcarbonMassBasisVariation,
    proposedPrizcarbonRadiusBasisVariation,
    proposedPrizcarbonMetricBasisVariation
  ]

end

end Chronos.Frontier
