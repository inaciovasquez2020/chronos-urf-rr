import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricFirstJet
import Chronos.Frontier.ReggeWheelerOddParityLinearizedRiemann

namespace Chronos.Frontier

noncomputable section

/--
A pointwise second coordinate jet of the odd-parity metric perturbation.

The first jet contains the metric and its coordinate first derivatives. The
new field contains `∂_κ ∂_λ h_{μν}`.
-/
structure ReggeWheelerOddParityMetricPerturbationSecondJet where
  firstJet : ReggeWheelerOddParityMetricPerturbationFirstJet
  metricSecondPartial :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ

/--
The radial derivative of the Schwarzschild exterior factor

`f(r) = 1 - 2M/r`.
-/
def reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) : ℝ :=
  2 * frame.background.mass /
    frame.background.radius ^ 2

/--
The second radial derivative of the Schwarzschild exterior factor.
-/
def reggeWheelerSchwarzschildExteriorFactorSecondRadialDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) : ℝ :=
  -4 * frame.background.mass /
    frame.background.radius ^ 3

/--
The second radial derivative of the inverse radial Schwarzschild component

`g^{rr}_covariant = 1/f`.

This separate definition avoids layout-sensitive local declarations inside
the coordinate-pattern match.
-/
def reggeWheelerSchwarzschildCovariantRadialMetricSecondRadialDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) : ℝ :=
  -reggeWheelerSchwarzschildExteriorFactorSecondRadialDerivative frame /
        (
          reggeWheelerSchwarzschildExteriorFactor frame.background
        ) ^ 2 +
    2 *
        (
          reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
            frame
        ) ^ 2 /
      (
        reggeWheelerSchwarzschildExteriorFactor frame.background
      ) ^ 3

/--
Coordinate derivatives of the inverse Schwarzschild metric.

Only radial derivatives occur, except for the theta derivative of
`g^{φφ}`.
-/
def reggeWheelerSchwarzschildInverseMetricComponentPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  | .radial, .time, .time =>
      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative frame /
        (
          reggeWheelerSchwarzschildExteriorFactor frame.background
        ) ^ 2

  | .radial, .radial, .radial =>
      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative frame

  | .radial, .theta, .theta =>
      -2 / frame.background.radius ^ 3

  | .radial, .phi, .phi =>
      -2 /
        (
          frame.background.radius ^ 3 *
            Real.sin frame.polarAngle ^ 2
        )

  | .theta, .phi, .phi =>
      -(2 * Real.cos frame.polarAngle) /
        (
          frame.background.radius ^ 2 *
            Real.sin frame.polarAngle ^ 3
        )

  | _, _, _ =>
      0

/--
The explicit second coordinate partials of the diagonal Schwarzschild metric.

The index order is `∂_κ ∂_λ g_{μν}`.
-/
def reggeWheelerSchwarzschildMetricSecondPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  if metricLeft = metricRight then
    match derivativeOuter, derivativeInner, metricLeft with
    | .radial, .radial, .time =>
        -reggeWheelerSchwarzschildExteriorFactorSecondRadialDerivative
          frame

    | .radial, .radial, .radial =>
        reggeWheelerSchwarzschildCovariantRadialMetricSecondRadialDerivative
          frame

    | .radial, .radial, .theta =>
        2

    | .radial, .radial, .phi =>
        2 * Real.sin frame.polarAngle ^ 2

    | .radial, .theta, .phi =>
        4 *
          frame.background.radius *
          Real.sin frame.polarAngle *
          Real.cos frame.polarAngle

    | .theta, .radial, .phi =>
        4 *
          frame.background.radius *
          Real.sin frame.polarAngle *
          Real.cos frame.polarAngle

    | .theta, .theta, .phi =>
        2 *
          frame.background.radius ^ 2 *
          (
            Real.cos frame.polarAngle ^ 2 -
              Real.sin frame.polarAngle ^ 2
          )

    | _, _, _ =>
        0
  else
    0

/--
The coordinate derivative of the background connection kernel

`K̄_{μνσ}
  = ∂_μ ḡ_{νσ}
    + ∂_ν ḡ_{μσ}
    - ∂_σ ḡ_{μν}`.
-/
def reggeWheelerSchwarzschildConnectionKernelPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSchwarzschildMetricSecondPartial
      frame derivative lowerLeft lowerRight contraction +
    reggeWheelerSchwarzschildMetricSecondPartial
      frame derivative lowerRight lowerLeft contraction -
    reggeWheelerSchwarzschildMetricSecondPartial
      frame derivative contraction lowerLeft lowerRight

/--
The coordinate derivative of the perturbation connection kernel

`K[h]_{μνσ}
  = ∂_μ h_{νσ}
    + ∂_ν h_{μσ}
    - ∂_σ h_{μν}`.
-/
def reggeWheelerOddParityPerturbationConnectionKernelPartial
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  jet.metricSecondPartial
      derivative lowerLeft lowerRight contraction +
    jet.metricSecondPartial
      derivative lowerRight lowerLeft contraction -
    jet.metricSecondPartial
      derivative contraction lowerLeft lowerRight

/--
The coordinate derivative of the first-order inverse metric

`δg^{ρσ} = -ḡ^{ρρ} h_{ρσ} ḡ^{σσ}`

for the diagonal Schwarzschild background.
-/
def reggeWheelerOddParityLinearizedInverseMetricComponentPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative upper contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  -(
    reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame derivative upper upper *
        jet.firstJet.metricValue upper contraction *
        reggeWheelerSchwarzschildInverseMetricComponent
          frame contraction contraction +

      reggeWheelerSchwarzschildInverseMetricComponent
          frame upper upper *
        jet.firstJet.metricPartial
          derivative upper contraction *
        reggeWheelerSchwarzschildInverseMetricComponent
          frame contraction contraction +

      reggeWheelerSchwarzschildInverseMetricComponent
          frame upper upper *
        jet.firstJet.metricValue upper contraction *
        reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame derivative contraction contraction
  )

/--
One product-rule summand in the coordinate derivative of the odd-parity
linearized Christoffel symbol.
-/
def reggeWheelerOddParityLinearizedChristoffelSummandPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative upper lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame jet derivative upper contraction *
      reggeWheelerSchwarzschildConnectionKernel
        frame lowerLeft lowerRight contraction +

    reggeWheelerOddParityLinearizedInverseMetricComponent
        frame jet.firstJet upper contraction *
      reggeWheelerSchwarzschildConnectionKernelPartial
        frame derivative lowerLeft lowerRight contraction +

    reggeWheelerSchwarzschildInverseMetricComponentPartial
        frame derivative upper contraction *
      reggeWheelerOddParityPerturbationConnectionKernel
        jet.firstJet lowerLeft lowerRight contraction +

    reggeWheelerSchwarzschildInverseMetricComponent
        frame upper contraction *
      reggeWheelerOddParityPerturbationConnectionKernelPartial
        jet derivative lowerLeft lowerRight contraction

/--
The coordinate derivative of the full odd-parity linearized Christoffel
symbol.

This is the product-rule derivative of the previously established connection
formula.
-/
def reggeWheelerOddParityLinearizedChristoffelPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  (1 / 2 : ℝ) *
    reggeWheelerSpacetimeCoordinateContraction
      (fun contraction =>
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          jet
          derivative
          upper
          lowerLeft
          lowerRight
          contraction)

/--
Construct the linearized-connection first jet from a metric second jet.

Unlike the earlier constructor, this definition accepts no arbitrary
four-index `connectionPartial` function.
-/
def reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet) :
    ReggeWheelerOddParityLinearizedConnectionFirstJet where
  connectionValue :=
    reggeWheelerOddParityLinearizedChristoffel
      frame jet.firstJet

  connectionPartial :=
    reggeWheelerOddParityLinearizedChristoffelPartial
      frame jet

  connectionValue_lower_symmetric :=
    reggeWheelerOddParityLinearizedChristoffel_lower_symmetric
      frame jet.firstJet

/--
The value field is exactly the previously derived linearized Christoffel
symbol.
-/
theorem
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet_connectionValue
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet) :
    (
      reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
        frame jet
    ).connectionValue =
      reggeWheelerOddParityLinearizedChristoffel
        frame jet.firstJet := by
  rfl

/--
The derivative field is exactly the product-rule coordinate derivative of
the linearized Christoffel symbol.
-/
theorem
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet_connectionPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet) :
    (
      reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
        frame jet
    ).connectionPartial =
      reggeWheelerOddParityLinearizedChristoffelPartial
        frame jet := by
  rfl

/--
A component-level form of the connection-partial reconstruction.
-/
theorem
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet_connectionPartial_apply
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
        frame jet
    ).connectionPartial
        derivative
        upper
        lowerLeft
        lowerRight =
      reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        jet
        derivative
        upper
        lowerLeft
        lowerRight := by
  rfl

def reggeWheelerOddParityDerivedLinearizedConnectionFirstJetBoundary :
    String :=
  "LINEARIZED_CONNECTION_FIRST_JET_DERIVED_BY_EXACT_PRODUCT_RULE_FROM_A_METRIC_SECOND_JET_WITHOUT_AN_ARBITRARY_CONNECTION_PARTIAL_FUNCTION_METRIC_SECOND_PARTIAL_REMAINS_SUPPLIED_AND_MUST_NEXT_BE_RECONSTRUCTED_FROM_A_CPM_THIRD_JET_AND_SECOND_ANGULAR_HARMONIC_DERIVATIVES_FREE_FALL_RESPONSE_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
