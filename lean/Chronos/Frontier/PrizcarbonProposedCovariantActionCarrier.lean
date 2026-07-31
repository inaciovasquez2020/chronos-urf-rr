import Chronos.Frontier.PrizcarbonR3ContinuumPotentialControl

namespace Chronos.Frontier

noncomputable section

/--
Scalar contractions used to evaluate the proposed covariant action density.

This is an explicit proposed carrier. It is not asserted to be an established
derivation of the existing Prizcarbon potential.
-/
structure ProposedPrizcarbonCovariantScalars where
  scalarCurvature : ℝ
  scalarKinetic : ℝ
  arealRadiusGradientSq : ℝ
  arealRadius : ℝ
  massAspect : ℝ
  pseudoscalar : ℝ
  multiplier : ℝ
  currentMassDerivative : ℝ

/-- Local scalar data required by the proposed Euler–Lagrange equations. -/
structure ProposedPrizcarbonEulerLagrangeJet where
  boxPseudoscalar : ℝ
  pseudoscalar : ℝ
  arealRadius : ℝ
  massAspect : ℝ
  arealRadiusGradientSq : ℝ
  massDerivative : ℝ
  currentDivergence : ℝ
  multiplier : ℝ
  multiplierRadiusGradientDivergence : ℝ
  einsteinTensorComponent : ℝ
  stressTensorComponent : ℝ

/-- Residuals of the proposed field equations. -/
structure ProposedPrizcarbonEulerLagrangeResiduals where
  scalar : ℝ
  radiusConstraint : ℝ
  massConstancy : ℝ
  mass : ℝ
  radius : ℝ
  metric : ℝ

def proposedPrizcarbonActionDensity
    (newtonCoupling r3 : ℝ)
    (x : ProposedPrizcarbonCovariantScalars) : ℝ :=
  x.scalarCurvature / (16 * Real.pi * newtonCoupling)
    - (1 / 2 : ℝ) * x.scalarKinetic
    - (1 / 2 : ℝ) * (r3 - 8) *
        x.massAspect / x.arealRadius ^ 3 * x.pseudoscalar ^ 2
    + x.multiplier *
        (x.arealRadiusGradientSq - 1 +
          2 * x.massAspect / x.arealRadius)
    + x.currentMassDerivative

def proposedPrizcarbonScalarEulerLagrangeResidual
    (r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  jet.boxPseudoscalar
    - (r3 - 8) * jet.massAspect /
        jet.arealRadius ^ 3 * jet.pseudoscalar

def proposedPrizcarbonRadiusConstraintResidual
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  jet.arealRadiusGradientSq
    - 1
    + 2 * jet.massAspect / jet.arealRadius

def proposedPrizcarbonMassConstancyResidual
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  jet.massDerivative

def proposedPrizcarbonMassEulerLagrangeResidual
    (r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  -jet.currentDivergence
    + 2 * jet.multiplier / jet.arealRadius
    - (1 / 2 : ℝ) * (r3 - 8) *
        jet.pseudoscalar ^ 2 / jet.arealRadius ^ 3

def proposedPrizcarbonRadiusEulerLagrangeResidual
    (r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  -2 * jet.multiplierRadiusGradientDivergence
    - 2 * jet.multiplier * jet.massAspect /
        jet.arealRadius ^ 2
    + (3 / 2 : ℝ) * (r3 - 8) *
        jet.massAspect * jet.pseudoscalar ^ 2 /
          jet.arealRadius ^ 4

def proposedPrizcarbonMetricEulerLagrangeResidual
    (newtonCoupling : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) : ℝ :=
  jet.einsteinTensorComponent
    - 8 * Real.pi * newtonCoupling *
        jet.stressTensorComponent

def proposedPrizcarbonEulerLagrangeResiduals
    (newtonCoupling r3 : ℝ)
    (jet : ProposedPrizcarbonEulerLagrangeJet) :
    ProposedPrizcarbonEulerLagrangeResiduals :=
  {
    scalar :=
      proposedPrizcarbonScalarEulerLagrangeResidual r3 jet
    radiusConstraint :=
      proposedPrizcarbonRadiusConstraintResidual jet
    massConstancy :=
      proposedPrizcarbonMassConstancyResidual jet
    mass :=
      proposedPrizcarbonMassEulerLagrangeResidual r3 jet
    radius :=
      proposedPrizcarbonRadiusEulerLagrangeResidual r3 jet
    metric :=
      proposedPrizcarbonMetricEulerLagrangeResidual
        newtonCoupling jet
  }

structure ProposedPrizcarbonCovariantActionCarrier where
  newtonCoupling : ℝ
  newtonCoupling_pos : 0 < newtonCoupling
  r3Coupling : ℝ
  actionDensity : ProposedPrizcarbonCovariantScalars → ℝ
  eulerLagrangeResiduals :
    ProposedPrizcarbonEulerLagrangeJet →
      ProposedPrizcarbonEulerLagrangeResiduals
  actionDensity_eq :
    actionDensity =
      proposedPrizcarbonActionDensity
        newtonCoupling r3Coupling
  eulerLagrangeResiduals_eq :
    eulerLagrangeResiduals =
      proposedPrizcarbonEulerLagrangeResiduals
        newtonCoupling r3Coupling

def proposedPrizcarbonCovariantActionCarrierOf
    (newtonCoupling r3 : ℝ)
    (hNewton : 0 < newtonCoupling) :
    ProposedPrizcarbonCovariantActionCarrier :=
  {
    newtonCoupling := newtonCoupling
    newtonCoupling_pos := hNewton
    r3Coupling := r3
    actionDensity :=
      proposedPrizcarbonActionDensity newtonCoupling r3
    eulerLagrangeResiduals :=
      proposedPrizcarbonEulerLagrangeResiduals
        newtonCoupling r3
    actionDensity_eq := rfl
    eulerLagrangeResiduals_eq := rfl
  }

def proposedPrizcarbonSchwarzschildLapse
    (mass radius : ℝ) : ℝ :=
  1 - 2 * mass / radius

def proposedPrizcarbonSchwarzschildBranchJet
    (mass radius : ℝ) :
    ProposedPrizcarbonEulerLagrangeJet :=
  {
    boxPseudoscalar := 0
    pseudoscalar := 0
    arealRadius := radius
    massAspect := mass
    arealRadiusGradientSq :=
      proposedPrizcarbonSchwarzschildLapse mass radius
    massDerivative := 0
    currentDivergence := 0
    multiplier := 0
    multiplierRadiusGradientDivergence := 0
    einsteinTensorComponent := 0
    stressTensorComponent := 0
  }

theorem proposedPrizcarbonSchwarzschildBranch_radiusGradientSq
    (mass radius : ℝ) :
    (proposedPrizcarbonSchwarzschildBranchJet mass radius).arealRadiusGradientSq =
      proposedPrizcarbonSchwarzschildLapse mass radius := by
  rfl

theorem proposedPrizcarbon_schwarzschildBranch_equations
    (newtonCoupling r3 mass radius : ℝ) :
    let residuals :=
      proposedPrizcarbonEulerLagrangeResiduals
        newtonCoupling r3
        (proposedPrizcarbonSchwarzschildBranchJet mass radius)
    residuals.scalar = 0 ∧
      residuals.radiusConstraint = 0 ∧
      residuals.massConstancy = 0 ∧
      residuals.mass = 0 ∧
      residuals.radius = 0 ∧
      residuals.metric = 0 := by
  simp [
    proposedPrizcarbonEulerLagrangeResiduals,
    proposedPrizcarbonSchwarzschildBranchJet,
    proposedPrizcarbonSchwarzschildLapse,
    proposedPrizcarbonScalarEulerLagrangeResidual,
    proposedPrizcarbonRadiusConstraintResidual,
    proposedPrizcarbonMassConstancyResidual,
    proposedPrizcarbonMassEulerLagrangeResidual,
    proposedPrizcarbonRadiusEulerLagrangeResidual,
    proposedPrizcarbonMetricEulerLagrangeResidual
  ]

def proposedPrizcarbonCandidateEllTwoMOverR3Coefficient
    (r3 : ℝ) : ℝ :=
  2 + (r3 - 8)

def proposedPrizcarbonCandidateEllTwoCompactPotential
    (r3 mass y : ℝ) : ℝ :=
  y ^ 2 * (1 - y) *
      (12 +
        proposedPrizcarbonCandidateEllTwoMOverR3Coefficient r3 * y) /
    (8 * mass ^ 2)

end

end Chronos.Frontier

namespace Chronos.Frontier

noncomputable section

/--
The coefficient generated by the proposed scalar carrier equals the existing
ell = 2 Prizcarbon compact-potential coefficient `r3 - 6`.

This is only an algebraic coefficient bridge. It does not identify the
pseudoscalar with the metric-derived odd-parity master field.
-/
theorem proposedPrizcarbon_candidateEllTwoCoefficient_bridge
    (r3 : ℝ) :
    proposedPrizcarbonCandidateEllTwoMOverR3Coefficient r3 =
      r3 - 6 := by
  unfold proposedPrizcarbonCandidateEllTwoMOverR3Coefficient
  ring

end

end Chronos.Frontier
