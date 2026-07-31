import Chronos.Frontier.PrizcarbonProposedCovariantActionCarrier
import Chronos.Frontier.ReggeWheelerOddParityMasterExtraction
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricSecondJet

namespace Chronos.Frontier

noncomputable section

/--
The complete eight-component Prizcarbon action-scalar value at an encoded
Schwarzschild vacuum background.

This closes only the zeroth-order basepoint. It does not define the
epsilon-linear or epsilon-quadratic metric-path coefficients.
-/
def prizcarbonSchwarzschildActionScalarBasePoint
    (background : ReggeWheelerSchwarzschildBackground) :
    ProposedPrizcarbonCovariantScalars where
  scalarCurvature := 0
  scalarKinetic := 0
  arealRadiusGradientSq :=
    proposedPrizcarbonSchwarzschildLapse
      background.mass
      background.radius
  arealRadius := background.radius
  massAspect := background.mass
  pseudoscalar := 0
  multiplier := 0
  currentMassDerivative := 0

/--
The Schwarzschild action-scalar basepoint satisfies the encoded
areal-radius constraint.
-/
theorem prizcarbonSchwarzschildActionScalarBasePoint_radiusConstraint
    (background : ReggeWheelerSchwarzschildBackground) :
    let x :=
      prizcarbonSchwarzschildActionScalarBasePoint background
    x.arealRadiusGradientSq - 1 +
        2 * x.massAspect / x.arealRadius =
      0 := by
  dsimp [
    prizcarbonSchwarzschildActionScalarBasePoint,
    proposedPrizcarbonSchwarzschildLapse
  ]
  ring

/--
The encoded local action density vanishes at the pure Schwarzschild
vacuum basepoint.
-/
theorem prizcarbonSchwarzschildActionScalarBasePoint_actionDensity_eq_zero
    (newtonCoupling r3 : ℝ)
    (background : ReggeWheelerSchwarzschildBackground) :
    proposedPrizcarbonActionDensity
        newtonCoupling
        r3
        (prizcarbonSchwarzschildActionScalarBasePoint background) =
      0 := by
  simp [
    proposedPrizcarbonActionDensity,
    prizcarbonSchwarzschildActionScalarBasePoint
  ]

/--
The Euler-Lagrange basepoint is the already encoded Schwarzschild branch
jet evaluated at the same mass and radius.
-/
def prizcarbonSchwarzschildEulerLagrangeBasePoint
    (background : ReggeWheelerSchwarzschildBackground) :
    ProposedPrizcarbonEulerLagrangeJet :=
  proposedPrizcarbonSchwarzschildBranchJet
    background.mass
    background.radius

/--
The action-scalar and Euler-Lagrange basepoints agree on the five fields
common to their current signatures.
-/
theorem prizcarbonSchwarzschildBasePoint_actionJet_coherence
    (background : ReggeWheelerSchwarzschildBackground) :
    let x :=
      prizcarbonSchwarzschildActionScalarBasePoint background
    let jet :=
      prizcarbonSchwarzschildEulerLagrangeBasePoint background
    x.arealRadius = jet.arealRadius ∧
      x.massAspect = jet.massAspect ∧
      x.arealRadiusGradientSq =
        jet.arealRadiusGradientSq ∧
      x.pseudoscalar = jet.pseudoscalar ∧
      x.multiplier = jet.multiplier := by
  simp [
    prizcarbonSchwarzschildActionScalarBasePoint,
    prizcarbonSchwarzschildEulerLagrangeBasePoint,
    proposedPrizcarbonSchwarzschildBranchJet
  ]

/--
Every encoded Euler-Lagrange residual vanishes at the same Schwarzschild
basepoint.
-/
theorem prizcarbonSchwarzschildEulerLagrangeBasePoint_equations
    (newtonCoupling r3 : ℝ)
    (background : ReggeWheelerSchwarzschildBackground) :
    let residuals :=
      proposedPrizcarbonEulerLagrangeResiduals
        newtonCoupling
        r3
        (prizcarbonSchwarzschildEulerLagrangeBasePoint background)
    residuals.scalar = 0 ∧
      residuals.radiusConstraint = 0 ∧
      residuals.massConstancy = 0 ∧
      residuals.mass = 0 ∧
      residuals.radius = 0 ∧
      residuals.metric = 0 := by
  simpa [
    prizcarbonSchwarzschildEulerLagrangeBasePoint
  ] using
    proposedPrizcarbon_schwarzschildBranch_equations
      newtonCoupling
      r3
      background.mass
      background.radius

/--
Extract the common Schwarzschild action-scalar basepoint from the
background stored by an existing Regge-Wheeler-gauge metric mode.
-/
def prizcarbonSchwarzschildActionScalarBasePointOfRWGaugeMetric
    (components : ReggeWheelerOddParityRWGaugeMetricComponents) :
    ProposedPrizcarbonCovariantScalars :=
  prizcarbonSchwarzschildActionScalarBasePoint
    components.background

theorem
    prizcarbonSchwarzschildActionScalarBasePointOfRWGaugeMetric_actionDensity
    (newtonCoupling r3 : ℝ)
    (components : ReggeWheelerOddParityRWGaugeMetricComponents) :
    proposedPrizcarbonActionDensity
        newtonCoupling
        r3
        (
          prizcarbonSchwarzschildActionScalarBasePointOfRWGaugeMetric
            components
        ) =
      0 := by
  simpa [
    prizcarbonSchwarzschildActionScalarBasePointOfRWGaugeMetric
  ] using
    prizcarbonSchwarzschildActionScalarBasePoint_actionDensity_eq_zero
      newtonCoupling
      r3
      components.background

/--
Extract the same basepoint from the Schwarzschild background stored by
the CPM third jet used to construct the odd-parity metric second jet.
-/
def prizcarbonSchwarzschildActionScalarBasePointOfCPMThirdJet
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) :
    ProposedPrizcarbonCovariantScalars :=
  prizcarbonSchwarzschildActionScalarBasePoint
    jet.secondJet.firstJet.background

theorem
    prizcarbonSchwarzschildActionScalarBasePointOfCPMThirdJet_actionDensity
    (newtonCoupling r3 : ℝ)
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) :
    proposedPrizcarbonActionDensity
        newtonCoupling
        r3
        (
          prizcarbonSchwarzschildActionScalarBasePointOfCPMThirdJet
            jet
        ) =
      0 := by
  simpa [
    prizcarbonSchwarzschildActionScalarBasePointOfCPMThirdJet
  ] using
    prizcarbonSchwarzschildActionScalarBasePoint_actionDensity_eq_zero
      newtonCoupling
      r3
      jet.secondJet.firstJet.background

/--
The completed object is the common epsilon-zero action basepoint only.
The metric-path first variation, second variation, and action Hessian
remain to be derived from explicit contractions.
-/
def prizcarbonSchwarzschildActionScalarBasePointBoundary : String :=
  "SCHWARZSCHILD_ACTION_SCALAR_BASEPOINT_COMPLETE_METRIC_PATH_FIRST_VARIATION_AND_SECOND_VARIATION_NOT_YET_DERIVED"

end

end Chronos.Frontier
