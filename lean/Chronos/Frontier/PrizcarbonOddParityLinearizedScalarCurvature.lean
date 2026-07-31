import Chronos.Frontier.PrizcarbonSchwarzschildActionScalarBasePoint
import Chronos.Frontier.ReggeWheelerOddParityLoweredLinearizedRiemann

namespace Chronos.Frontier

noncomputable section

/--
The Schwarzschild Ricci contraction obtained directly from the existing
mixed-index background Riemann tensor:

`R̄_{σν} = R̄^ρ_{σρν}`.

The repeated coordinate is summed with the repository's explicit
four-coordinate contraction.
-/
def prizcarbonSchwarzschildRicciContraction
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet : ReggeWheelerSchwarzschildConnectionFirstJet)
    (transported curvatureRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun contracted =>
      reggeWheelerSchwarzschildRiemann
        frame
        connectionJet
        contracted
        transported
        contracted
        curvatureRight)

/--
The odd-parity linearized Ricci contraction obtained directly from the
existing mixed-index linearized Riemann tensor:

`δR_{σν} = δR^ρ_{σρν}`.
-/
def prizcarbonOddParityLinearizedRicciContraction
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (transported curvatureRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun contracted =>
      reggeWheelerOddParityLinearizedRiemann
        frame
        connectionJet
        contracted
        transported
        contracted
        curvatureRight)

/--
The contribution to the scalar-curvature first variation from varying the
inverse metric:

`δg^{μν} R̄_{μν}`.
-/
def prizcarbonOddParityInverseMetricBackgroundRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun left =>
      reggeWheelerSpacetimeCoordinateContraction
        (fun right =>
          reggeWheelerOddParityLinearizedInverseMetricComponent
                frame
                metricJet
                left
                right *
            prizcarbonSchwarzschildRicciContraction
              frame
              backgroundConnectionJet
              left
              right))

/--
The contribution to the scalar-curvature first variation from varying the
Ricci tensor:

`ḡ^{μν} δR_{μν}`.
-/
def prizcarbonOddParityBackgroundMetricLinearizedRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun left =>
      reggeWheelerSpacetimeCoordinateContraction
        (fun right =>
          reggeWheelerSchwarzschildInverseMetricComponent
                frame
                left
                right *
            prizcarbonOddParityLinearizedRicciContraction
              frame
              linearizedConnectionJet
              left
              right))

/--
The complete first variation of scalar curvature assembled from the two
required product-rule contributions:

`δR = δg^{μν} R̄_{μν} + ḡ^{μν} δR_{μν}`.

This is derived from the repository's metric, inverse-metric, background
Riemann, and linearized Riemann definitions. Its value is not set to zero by
definition.
-/
def prizcarbonOddParityLinearizedScalarCurvature
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) : ℝ :=
  prizcarbonOddParityInverseMetricBackgroundRicciContribution
      frame
      metricJet
      backgroundConnectionJet +
    prizcarbonOddParityBackgroundMetricLinearizedRicciContribution
      frame
      linearizedConnectionJet

/--
The scalar-curvature first variation expands into exactly its inverse-metric
and Ricci-variation contractions.
-/
theorem prizcarbonOddParityLinearizedScalarCurvature_eq_contributions
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) :
    prizcarbonOddParityLinearizedScalarCurvature
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet =
      prizcarbonOddParityInverseMetricBackgroundRicciContribution
          frame
          metricJet
          backgroundConnectionJet +
        prizcarbonOddParityBackgroundMetricLinearizedRicciContribution
          frame
          linearizedConnectionJet := by
  rfl

/--
The explicit first-order scalar-curvature polynomial with Schwarzschild
base value zero and coefficient given by the full contraction above.

This is only the first-order scalar-curvature sector. It is not a complete
metric-to-action-scalars path.
-/
def prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
    (epsilon : ℝ)
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) : ℝ :=
  epsilon *
    prizcarbonOddParityLinearizedScalarCurvature
      frame
      metricJet
      backgroundConnectionJet
      linearizedConnectionJet

@[simp]
theorem prizcarbonOddParityScalarCurvatureFirstOrderPolynomial_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) :
    prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
        0
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet =
      0 := by
  simp [
    prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
  ]

@[simp]
theorem prizcarbonOddParityScalarCurvatureFirstOrderPolynomial_one
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet) :
    prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
        1
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet =
      prizcarbonOddParityLinearizedScalarCurvature
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet := by
  simp [
    prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
  ]

/--
The scalar-curvature first-variation contraction is now explicit. Proving
that it vanishes for the concrete vacuum CPM metric jet still requires
component-level Ricci identities or an equivalent proved cancellation.
-/
def prizcarbonOddParityLinearizedScalarCurvatureBoundary : String :=
  "LINEARIZED_SCALAR_CURVATURE_CONTRACTION_COMPLETE_VACUUM_ODD_PARITY_ZERO_NOT_YET_PROVED_OTHER_ACTION_SCALAR_VARIATIONS_AND_ACTION_HESSIAN_REMAIN_OPEN"

end

end Chronos.Frontier
