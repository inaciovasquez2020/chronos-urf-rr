import Mathlib
import Chronos.Frontier.ReggeWheelerSchwarzschildCoordinateConnection

namespace Chronos.Frontier

noncomputable section

/--
A pointwise first coordinate jet of a symmetric metric perturbation.

The carrier records:

* the perturbation components `h_{μν}`;
* their coordinate derivatives `∂_κ h_{μν}`;
* symmetry in the two metric indices.

It does not assume field equations or choose a time/radial profile.
-/
structure ReggeWheelerOddParityMetricPerturbationFirstJet where
  metricValue :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ℝ
  metricPartial :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  metricValue_symmetric :
    ∀ left right,
      metricValue left right =
        metricValue right left
  metricPartial_symmetric :
    ∀ derivative left right,
      metricPartial derivative left right =
        metricPartial derivative right left

/--
Construct a first jet whose metric value is the assembled odd-parity
Regge–Wheeler metric mode.

The coordinate derivatives remain supplied data. Their metric-index symmetry
is the only condition imposed here.
-/
def reggeWheelerOddParityMetricPerturbationFirstJetOfMode
    (components : ReggeWheelerOddParityRWGaugeMetricComponents)
    (harmonic : ReggeWheelerOddParityAngularHarmonicValue)
    (metricPartial :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ)
    (partialSymmetry :
      ∀ derivative left right,
        metricPartial derivative left right =
          metricPartial derivative right left) :
    ReggeWheelerOddParityMetricPerturbationFirstJet where
  metricValue :=
    reggeWheelerOddParitySpacetimeMetricPerturbation
      components harmonic
  metricPartial := metricPartial
  metricValue_symmetric :=
    reggeWheelerOddParitySpacetimeMetricPerturbation_symmetric
      components harmonic
  metricPartial_symmetric := partialSymmetry

/--
The full inverse Schwarzschild metric components. The background is diagonal.
-/
def reggeWheelerSchwarzschildInverseMetricComponent
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ℝ
  | .time, .time =>
      reggeWheelerSchwarzschildInverseMetricDiagonal
        frame .time
  | .radial, .radial =>
      reggeWheelerSchwarzschildInverseMetricDiagonal
        frame .radial
  | .theta, .theta =>
      reggeWheelerSchwarzschildInverseMetricDiagonal
        frame .theta
  | .phi, .phi =>
      reggeWheelerSchwarzschildInverseMetricDiagonal
        frame .phi
  | _, _ => 0

theorem reggeWheelerSchwarzschildInverseMetricComponent_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (left right : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponent
        frame left right =
      reggeWheelerSchwarzschildInverseMetricComponent
        frame right left := by
  cases left <;> cases right <;>
    rfl

/--
The first variation of the inverse metric on the diagonal Schwarzschild
background:

`δg^{ρσ} = -g^{ρρ} h_{ρσ} g^{σσ}`.
-/
def reggeWheelerOddParityLinearizedInverseMetricComponent
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (left right : ReggeWheelerSpacetimeCoordinate) : ℝ :=
  -(
    reggeWheelerSchwarzschildInverseMetricDiagonal frame left *
      jet.metricValue left right *
      reggeWheelerSchwarzschildInverseMetricDiagonal frame right
  )

/-- The inverse-metric variation is symmetric. -/
theorem
    reggeWheelerOddParityLinearizedInverseMetricComponent_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (left right : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
        frame jet left right =
      reggeWheelerOddParityLinearizedInverseMetricComponent
        frame jet right left := by
  unfold reggeWheelerOddParityLinearizedInverseMetricComponent
  rw [jet.metricValue_symmetric left right]
  ring

/-- Finite contraction over the four Schwarzschild coordinate labels. -/
def reggeWheelerSpacetimeCoordinateContraction
    (term : ReggeWheelerSpacetimeCoordinate → ℝ) : ℝ :=
  term .time +
    term .radial +
    term .theta +
    term .phi

/--
Pointwise equality of coordinate-indexed terms is preserved by the explicit
four-coordinate contraction.
-/
theorem reggeWheelerSpacetimeCoordinateContraction_congr
    (left right : ReggeWheelerSpacetimeCoordinate → ℝ)
    (hPointwise : ∀ coordinate, left coordinate = right coordinate) :
    reggeWheelerSpacetimeCoordinateContraction left =
      reggeWheelerSpacetimeCoordinateContraction right := by
  unfold reggeWheelerSpacetimeCoordinateContraction
  rw [
    hPointwise .time,
    hPointwise .radial,
    hPointwise .theta,
    hPointwise .phi
  ]

/--
The background metric-derivative kernel occurring in the Christoffel formula.
-/
def reggeWheelerSchwarzschildConnectionKernel
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSchwarzschildMetricPartial
      frame lowerLeft lowerRight contraction +
    reggeWheelerSchwarzschildMetricPartial
      frame lowerRight lowerLeft contraction -
    reggeWheelerSchwarzschildMetricPartial
      frame contraction lowerLeft lowerRight

/--
The background connection kernel is symmetric in the two lower indices.
-/
theorem reggeWheelerSchwarzschildConnectionKernel_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildConnectionKernel
        frame lowerLeft lowerRight contraction =
      reggeWheelerSchwarzschildConnectionKernel
        frame lowerRight lowerLeft contraction := by
  unfold reggeWheelerSchwarzschildConnectionKernel
  rw [
    reggeWheelerSchwarzschildMetricPartial_symmetric
      frame contraction lowerLeft lowerRight
  ]
  ring

/-- The corresponding first-variation metric-derivative kernel. -/
def reggeWheelerOddParityPerturbationConnectionKernel
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  jet.metricPartial lowerLeft lowerRight contraction +
    jet.metricPartial lowerRight lowerLeft contraction -
    jet.metricPartial contraction lowerLeft lowerRight

/--
The perturbation connection kernel is symmetric in the lower indices.
-/
theorem
    reggeWheelerOddParityPerturbationConnectionKernel_lower_symmetric
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernel
        jet lowerLeft lowerRight contraction =
      reggeWheelerOddParityPerturbationConnectionKernel
        jet lowerRight lowerLeft contraction := by
  unfold reggeWheelerOddParityPerturbationConnectionKernel
  rw [
    jet.metricPartial_symmetric
      contraction lowerLeft lowerRight
  ]
  ring

/--
One contraction summand in the first variation of the Christoffel symbol.

It contains:

* the inverse-metric variation times the background metric kernel;
* the background inverse metric times the perturbation derivative kernel.
-/
def reggeWheelerOddParityLinearizedChristoffelSummand
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (upper lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerOddParityLinearizedInverseMetricComponent
      frame jet upper contraction *
    reggeWheelerSchwarzschildConnectionKernel
      frame lowerLeft lowerRight contraction +
  reggeWheelerSchwarzschildInverseMetricComponent
      frame upper contraction *
    reggeWheelerOddParityPerturbationConnectionKernel
      jet lowerLeft lowerRight contraction

/--
Every contraction summand is symmetric in the two lower indices.
-/
theorem
    reggeWheelerOddParityLinearizedChristoffelSummand_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (upper lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummand
        frame jet upper lowerLeft lowerRight contraction =
      reggeWheelerOddParityLinearizedChristoffelSummand
        frame jet upper lowerRight lowerLeft contraction := by
  unfold reggeWheelerOddParityLinearizedChristoffelSummand
  rw [
    reggeWheelerSchwarzschildConnectionKernel_lower_symmetric
      frame lowerLeft lowerRight contraction,
    reggeWheelerOddParityPerturbationConnectionKernel_lower_symmetric
      jet lowerLeft lowerRight contraction
  ]

/--
The first variation of the Schwarzschild Christoffel symbol:

`δΓ^ρ_{μν}
  = 1/2 δg^{ρσ}
      (∂_μ g_{νσ} + ∂_ν g_{μσ} - ∂_σ g_{μν})
    + 1/2 g^{ρσ}
      (∂_μ h_{νσ} + ∂_ν h_{μσ} - ∂_σ h_{μν})`.

The `σ` contraction is the explicit four-coordinate sum.
-/
def reggeWheelerOddParityLinearizedChristoffel
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  (1 / 2 : ℝ) *
    reggeWheelerSpacetimeCoordinateContraction
      (fun contraction =>
        reggeWheelerOddParityLinearizedChristoffelSummand
          frame jet upper lowerLeft lowerRight contraction)

/--
The odd-parity linearized Christoffel symbol is symmetric in its lower
indices. Thus the first-order connection remains torsion free.
-/
theorem reggeWheelerOddParityLinearizedChristoffel_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedChristoffel
        frame jet upper lowerLeft lowerRight =
      reggeWheelerOddParityLinearizedChristoffel
        frame jet upper lowerRight lowerLeft := by
  have hContraction :
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedChristoffelSummand
              frame jet upper lowerLeft lowerRight contraction) =
        reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedChristoffelSummand
              frame jet upper lowerRight lowerLeft contraction) := by
    exact
      reggeWheelerSpacetimeCoordinateContraction_congr
        (fun contraction =>
          reggeWheelerOddParityLinearizedChristoffelSummand
            frame jet upper lowerLeft lowerRight contraction)
        (fun contraction =>
          reggeWheelerOddParityLinearizedChristoffelSummand
            frame jet upper lowerRight lowerLeft contraction)
        (fun contraction =>
          reggeWheelerOddParityLinearizedChristoffelSummand_lower_symmetric
            frame jet upper lowerLeft lowerRight contraction)
  exact congrArg (fun value : ℝ => (1 / 2 : ℝ) * value) hContraction

def reggeWheelerOddParityLinearizedConnectionBoundary : String :=
  "ODD_PARITY_METRIC_FIRST_JET_AND_TORSION_FREE_LINEARIZED_CONNECTION_PROVED_COORDINATE_DERIVATIVES_NOT_YET_DERIVED_FROM_MASTER_EVOLUTION_LINEARIZED_RIEMANN_TIDAL_PROJECTION_GEODESIC_DEVIATION_AND_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
