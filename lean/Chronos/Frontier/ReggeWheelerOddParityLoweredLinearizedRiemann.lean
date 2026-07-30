import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityLinearizedRiemann

namespace Chronos.Frontier

noncomputable section

/--
A first coordinate jet of the background Schwarzschild connection.

The connection itself is the previously derived Schwarzschild Christoffel
symbol. Its coordinate derivatives remain supplied data.
-/
structure ReggeWheelerSchwarzschildConnectionFirstJet where
  connectionPartial :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ

/--
The quadratic connection summand in the mixed-index background Riemann
tensor.
-/
def reggeWheelerSchwarzschildRiemannSummand
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (upper transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSchwarzschildChristoffel
      frame upper curvatureLeft contraction *
    reggeWheelerSchwarzschildChristoffel
      frame contraction curvatureRight transported -
  reggeWheelerSchwarzschildChristoffel
      frame upper curvatureRight contraction *
    reggeWheelerSchwarzschildChristoffel
      frame contraction curvatureLeft transported

/--
The background Riemann contraction summand is antisymmetric in its two
curvature indices.
-/
theorem
    reggeWheelerSchwarzschildRiemannSummand_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (upper transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildRiemannSummand
        frame upper transported curvatureLeft curvatureRight contraction =
      -reggeWheelerSchwarzschildRiemannSummand
        frame upper transported curvatureRight curvatureLeft contraction := by
  unfold reggeWheelerSchwarzschildRiemannSummand
  ring

/--
The mixed-index background Schwarzschild Riemann tensor:

`R̄^ρ_{σμν}
  = ∂_μ Γ̄^ρ_{νσ} - ∂_ν Γ̄^ρ_{μσ}
    + Γ̄^ρ_{μλ} Γ̄^λ_{νσ}
    - Γ̄^ρ_{νλ} Γ̄^λ_{μσ}`.
-/
def reggeWheelerSchwarzschildRiemann
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet : ReggeWheelerSchwarzschildConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  connectionJet.connectionPartial
      curvatureLeft upper curvatureRight transported -
    connectionJet.connectionPartial
      curvatureRight upper curvatureLeft transported +
    reggeWheelerSpacetimeCoordinateContraction
      (fun contraction =>
        reggeWheelerSchwarzschildRiemannSummand
          frame upper transported
          curvatureLeft curvatureRight contraction)

/--
The mixed-index background Riemann tensor is antisymmetric in its two
curvature indices.
-/
theorem
    reggeWheelerSchwarzschildRiemann_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet : ReggeWheelerSchwarzschildConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildRiemann
        frame connectionJet upper transported
        curvatureLeft curvatureRight =
      -reggeWheelerSchwarzschildRiemann
        frame connectionJet upper transported
        curvatureRight curvatureLeft := by
  have hPointwise :
      ∀ contraction,
        reggeWheelerSchwarzschildRiemannSummand
            frame upper transported
            curvatureLeft curvatureRight contraction =
          -reggeWheelerSchwarzschildRiemannSummand
            frame upper transported
            curvatureRight curvatureLeft contraction := by
    intro contraction
    exact
      reggeWheelerSchwarzschildRiemannSummand_curvatureIndices_antisymmetric
        frame upper transported
        curvatureLeft curvatureRight contraction

  have hContraction :
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerSchwarzschildRiemannSummand
              frame upper transported
              curvatureLeft curvatureRight contraction) =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerSchwarzschildRiemannSummand
              frame upper transported
              curvatureRight curvatureLeft contraction) := by
    calc
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerSchwarzschildRiemannSummand
              frame upper transported
              curvatureLeft curvatureRight contraction)
          =
        reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            -reggeWheelerSchwarzschildRiemannSummand
              frame upper transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_congr
                (fun contraction =>
                  reggeWheelerSchwarzschildRiemannSummand
                    frame upper transported
                    curvatureLeft curvatureRight contraction)
                (fun contraction =>
                  -reggeWheelerSchwarzschildRiemannSummand
                    frame upper transported
                    curvatureRight curvatureLeft contraction)
                hPointwise
      _ =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerSchwarzschildRiemannSummand
              frame upper transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_neg
                (fun contraction =>
                  reggeWheelerSchwarzschildRiemannSummand
                    frame upper transported
                    curvatureRight curvatureLeft contraction)

  unfold reggeWheelerSchwarzschildRiemann
  rw [hContraction]
  ring

/--
One contraction summand in the full first variation of the covariant Riemann
tensor:

`δR_{αβμν}
  = h_{αρ} R̄^ρ_{βμν}
    + ḡ_{αρ} δR^ρ_{βμν}`.

Both terms are required because lowering the first index also varies the
metric.
-/
def reggeWheelerOddParityLoweredLinearizedRiemannSummand
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (lowered transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  metricJet.metricValue lowered contraction *
    reggeWheelerSchwarzschildRiemann
      frame backgroundConnectionJet contraction transported
      curvatureLeft curvatureRight +
  reggeWheelerSchwarzschildMetricComponent
      frame lowered contraction *
    reggeWheelerOddParityLinearizedRiemann
      frame linearizedConnectionJet contraction transported
      curvatureLeft curvatureRight

/--
Each lowering contraction summand is antisymmetric in the curvature indices.
-/
theorem
    reggeWheelerOddParityLoweredLinearizedRiemannSummand_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (lowered transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLoweredLinearizedRiemannSummand
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureLeft curvatureRight contraction =
      -reggeWheelerOddParityLoweredLinearizedRiemannSummand
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureRight curvatureLeft contraction := by
  unfold reggeWheelerOddParityLoweredLinearizedRiemannSummand
  rw [
    reggeWheelerSchwarzschildRiemann_curvatureIndices_antisymmetric
      frame backgroundConnectionJet contraction transported
      curvatureLeft curvatureRight,
    reggeWheelerOddParityLinearizedRiemann_curvatureIndices_antisymmetric
      frame linearizedConnectionJet contraction transported
      curvatureLeft curvatureRight
  ]
  ring

/--
The complete covariant odd-parity linearized Riemann tensor.

This includes both:

* the perturbed metric lowering the background Riemann tensor;
* the background metric lowering the mixed-index linearized Riemann tensor.
-/
def reggeWheelerOddParityLoweredLinearizedRiemann
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (lowered transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun contraction =>
      reggeWheelerOddParityLoweredLinearizedRiemannSummand
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureLeft curvatureRight contraction)

/--
The fully lowered odd-parity linearized Riemann tensor is antisymmetric in its
two curvature indices.
-/
theorem
    reggeWheelerOddParityLoweredLinearizedRiemann_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (lowered transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLoweredLinearizedRiemann
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureLeft curvatureRight =
      -reggeWheelerOddParityLoweredLinearizedRiemann
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureRight curvatureLeft := by
  have hPointwise :
      ∀ contraction,
        reggeWheelerOddParityLoweredLinearizedRiemannSummand
            frame metricJet backgroundConnectionJet linearizedConnectionJet
            lowered transported curvatureLeft curvatureRight contraction =
          -reggeWheelerOddParityLoweredLinearizedRiemannSummand
            frame metricJet backgroundConnectionJet linearizedConnectionJet
            lowered transported curvatureRight curvatureLeft contraction := by
    intro contraction
    exact
      reggeWheelerOddParityLoweredLinearizedRiemannSummand_curvatureIndices_antisymmetric
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvatureLeft curvatureRight contraction

  have hContraction :
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLoweredLinearizedRiemannSummand
              frame metricJet backgroundConnectionJet
              linearizedConnectionJet lowered transported
              curvatureLeft curvatureRight contraction) =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLoweredLinearizedRiemannSummand
              frame metricJet backgroundConnectionJet
              linearizedConnectionJet lowered transported
              curvatureRight curvatureLeft contraction) := by
    calc
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLoweredLinearizedRiemannSummand
              frame metricJet backgroundConnectionJet
              linearizedConnectionJet lowered transported
              curvatureLeft curvatureRight contraction)
          =
        reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            -reggeWheelerOddParityLoweredLinearizedRiemannSummand
              frame metricJet backgroundConnectionJet
              linearizedConnectionJet lowered transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_congr
                (fun contraction =>
                  reggeWheelerOddParityLoweredLinearizedRiemannSummand
                    frame metricJet backgroundConnectionJet
                    linearizedConnectionJet lowered transported
                    curvatureLeft curvatureRight contraction)
                (fun contraction =>
                  -reggeWheelerOddParityLoweredLinearizedRiemannSummand
                    frame metricJet backgroundConnectionJet
                    linearizedConnectionJet lowered transported
                    curvatureRight curvatureLeft contraction)
                hPointwise
      _ =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLoweredLinearizedRiemannSummand
              frame metricJet backgroundConnectionJet
              linearizedConnectionJet lowered transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_neg
                (fun contraction =>
                  reggeWheelerOddParityLoweredLinearizedRiemannSummand
                    frame metricJet backgroundConnectionJet
                    linearizedConnectionJet lowered transported
                    curvatureRight curvatureLeft contraction)

  unfold reggeWheelerOddParityLoweredLinearizedRiemann
  exact hContraction

/--
A fully lowered linearized Riemann component with repeated curvature indices
vanishes.
-/
theorem
    reggeWheelerOddParityLoweredLinearizedRiemann_curvatureDiagonal_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (lowered transported curvature :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLoweredLinearizedRiemann
        frame metricJet backgroundConnectionJet linearizedConnectionJet
        lowered transported curvature curvature =
      0 := by
  have hAntisymmetric :=
    reggeWheelerOddParityLoweredLinearizedRiemann_curvatureIndices_antisymmetric
      frame metricJet backgroundConnectionJet linearizedConnectionJet
      lowered transported curvature curvature
  linarith

def reggeWheelerOddParityLoweredLinearizedRiemannBoundary : String :=
  "FULL_COVARIANT_ODD_PARITY_LINEARIZED_RIEMANN_INCLUDING_H_TIMES_BACKGROUND_RIEMANN_AND_BACKGROUND_METRIC_TIMES_DELTA_RIEMANN_PROVED_BACKGROUND_AND_LINEARIZED_CONNECTION_DERIVATIVES_REMAIN_SUPPLIED_JET_DATA_DETECTOR_TIDAL_PROJECTION_GEODESIC_DEVIATION_AND_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
