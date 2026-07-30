import Mathlib
import Chronos.Frontier.ReggeWheelerSchwarzschildStaticDetectorFrame

namespace Chronos.Frontier

noncomputable section

/--
The radial derivative of the Schwarzschild exterior factor

`f(r) = 1 - 2M/r`:

`∂ᵣf = 2M/r²`.
-/
def reggeWheelerSchwarzschildExteriorFactorRadialDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) : ℝ :=
  2 * frame.background.mass / frame.background.radius ^ 2

/-- Coordinate components of the Schwarzschild metric. -/
def reggeWheelerSchwarzschildMetricComponent
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ℝ
  | .time, .time =>
      -reggeWheelerSchwarzschildExteriorFactor frame.background
  | .radial, .radial =>
      1 /
        reggeWheelerSchwarzschildExteriorFactor frame.background
  | .theta, .theta =>
      frame.background.radius ^ 2
  | .phi, .phi =>
      (frame.background.radius *
        Real.sin frame.polarAngle) ^ 2
  | _, _ => 0

theorem reggeWheelerSchwarzschildMetricComponent_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (left right : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildMetricComponent frame left right =
      reggeWheelerSchwarzschildMetricComponent frame right left := by
  cases left <;> cases right <;>
    rfl

/-- Nonzero diagonal entries of the inverse Schwarzschild metric. -/
def reggeWheelerSchwarzschildInverseMetricDiagonal
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeCoordinate → ℝ
  | .time =>
      -(1 /
        reggeWheelerSchwarzschildExteriorFactor frame.background)
  | .radial =>
      reggeWheelerSchwarzschildExteriorFactor frame.background
  | .theta =>
      1 / frame.background.radius ^ 2
  | .phi =>
      1 /
        (frame.background.radius *
          Real.sin frame.polarAngle) ^ 2

/--
The coordinate partial derivatives `∂_κ g_{μν}` of the diagonal
Schwarzschild metric.
-/
def reggeWheelerSchwarzschildMetricPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  | .radial, .time, .time =>
      -reggeWheelerSchwarzschildExteriorFactorRadialDerivative frame
  | .radial, .radial, .radial =>
      -reggeWheelerSchwarzschildExteriorFactorRadialDerivative frame /
        reggeWheelerSchwarzschildExteriorFactor frame.background ^ 2
  | .radial, .theta, .theta =>
      2 * frame.background.radius
  | .radial, .phi, .phi =>
      2 * frame.background.radius *
        Real.sin frame.polarAngle ^ 2
  | .theta, .phi, .phi =>
      2 * frame.background.radius ^ 2 *
        Real.sin frame.polarAngle *
        Real.cos frame.polarAngle
  | _, _, _ => 0

theorem reggeWheelerSchwarzschildMetricPartial_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivative left right : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildMetricPartial
        frame derivative left right =
      reggeWheelerSchwarzschildMetricPartial
        frame derivative right left := by
  cases derivative <;>
    cases left <;>
      cases right <;>
        rfl

/--
The Schwarzschild Christoffel symbol obtained from the diagonal inverse metric
and explicit metric derivatives:

`Γ^ρ_{μν}
  = 1/2 g^{ρρ}
      (∂_μ g_{νρ} + ∂_ν g_{μρ} - ∂_ρ g_{μν})`.
-/
def reggeWheelerSchwarzschildChristoffel
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  (1 / 2 : ℝ) *
    reggeWheelerSchwarzschildInverseMetricDiagonal frame upper *
    (
      reggeWheelerSchwarzschildMetricPartial
        frame lowerLeft lowerRight upper +
      reggeWheelerSchwarzschildMetricPartial
        frame lowerRight lowerLeft upper -
      reggeWheelerSchwarzschildMetricPartial
        frame upper lowerLeft lowerRight
    )

/--
The metric-derived coordinate connection is symmetric in its lower indices.
-/
theorem reggeWheelerSchwarzschildChristoffel_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildChristoffel
        frame upper lowerLeft lowerRight =
      reggeWheelerSchwarzschildChristoffel
        frame upper lowerRight lowerLeft := by
  unfold reggeWheelerSchwarzschildChristoffel
  rw [
    reggeWheelerSchwarzschildMetricPartial_symmetric
      frame upper lowerRight lowerLeft
  ]
  ring

private theorem half_negative_reciprocal_negative
    (factor derivative : ℝ)
    (factor_ne_zero : factor ≠ 0) :
    (1 / 2 : ℝ) *
          (-(1 / factor)) *
          (-derivative) =
      derivative / (2 * factor) := by
  field_simp [factor_ne_zero]

private theorem half_product_eq_div_two
    (left right : ℝ) :
    (1 / 2 : ℝ) * left * right =
      left * right / 2 := by
  ring

private theorem half_product_negative_double
    (factor radius : ℝ) :
    (1 / 2 : ℝ) *
          factor *
          (-(2 * radius)) =
      -radius * factor := by
  ring

/-- The explicit `Γᵗ_{tr}` component. -/
theorem reggeWheelerSchwarzschildChristoffel_time_time_radial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildChristoffel
        frame .time .time .radial =
      reggeWheelerSchwarzschildExteriorFactorRadialDerivative frame /
        (
          2 *
            reggeWheelerSchwarzschildExteriorFactor
              frame.background
        ) := by
  have hFactor :
      reggeWheelerSchwarzschildExteriorFactor
          frame.background ≠ 0 :=
    reggeWheelerSchwarzschildExteriorFactor_ne_zero
      frame.background
  simpa [
    reggeWheelerSchwarzschildChristoffel,
    reggeWheelerSchwarzschildInverseMetricDiagonal,
    reggeWheelerSchwarzschildMetricPartial
  ] using
    half_negative_reciprocal_negative
      (reggeWheelerSchwarzschildExteriorFactor
        frame.background)
      (reggeWheelerSchwarzschildExteriorFactorRadialDerivative
        frame)
      hFactor

/-- The explicit `Γʳ_{tt}` component. -/
theorem reggeWheelerSchwarzschildChristoffel_radial_time_time
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildChristoffel
        frame .radial .time .time =
      (
        reggeWheelerSchwarzschildExteriorFactor frame.background *
          reggeWheelerSchwarzschildExteriorFactorRadialDerivative frame
      ) /
        2 := by
  simpa [
    reggeWheelerSchwarzschildChristoffel,
    reggeWheelerSchwarzschildInverseMetricDiagonal,
    reggeWheelerSchwarzschildMetricPartial
  ] using
    half_product_eq_div_two
      (reggeWheelerSchwarzschildExteriorFactor
        frame.background)
      (reggeWheelerSchwarzschildExteriorFactorRadialDerivative
        frame)

/-- The explicit `Γʳ_{θθ}` component. -/
theorem reggeWheelerSchwarzschildChristoffel_radial_theta_theta
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildChristoffel
        frame .radial .theta .theta =
      -frame.background.radius *
        reggeWheelerSchwarzschildExteriorFactor frame.background := by
  simpa [
    reggeWheelerSchwarzschildChristoffel,
    reggeWheelerSchwarzschildInverseMetricDiagonal,
    reggeWheelerSchwarzschildMetricPartial
  ] using
    half_product_negative_double
      (reggeWheelerSchwarzschildExteriorFactor
        frame.background)
      frame.background.radius

def reggeWheelerSchwarzschildCoordinateConnectionBoundary : String :=
  "SCHWARZSCHILD_METRIC_PARTIALS_AND_TORSION_FREE_COORDINATE_CONNECTION_DERIVED_LINEARIZED_PERTURBATION_CONNECTION_RIEMANN_PROJECTION_GEODESIC_DEVIATION_AND_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
