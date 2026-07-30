import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityLinearizedConnection

namespace Chronos.Frontier

noncomputable section

/--
A first coordinate jet of the odd-parity linearized connection.

The connection value is the previously derived `δΓ`. Its coordinate
derivatives remain supplied data. No master-field evolution equation is
introduced at this stage.
-/
structure ReggeWheelerOddParityLinearizedConnectionFirstJet where
  connectionValue :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  connectionPartial :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ
  connectionValue_lower_symmetric :
    ∀ upper lowerLeft lowerRight,
      connectionValue upper lowerLeft lowerRight =
        connectionValue upper lowerRight lowerLeft

/--
Construct a connection first jet from the derived odd-parity linearized
Christoffel symbol and supplied coordinate derivatives.
-/
def reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricJet
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (connectionPartial :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ) :
    ReggeWheelerOddParityLinearizedConnectionFirstJet where
  connectionValue :=
    reggeWheelerOddParityLinearizedChristoffel frame metricJet
  connectionPartial := connectionPartial
  connectionValue_lower_symmetric :=
    reggeWheelerOddParityLinearizedChristoffel_lower_symmetric
      frame metricJet

/--
The product-rule contraction summand in the first variation of

`Γ^ρ_{μλ} Γ^λ_{νσ} - Γ^ρ_{νλ} Γ^λ_{μσ}`.
-/
def reggeWheelerOddParityLinearizedRiemannSummand
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  connectionJet.connectionValue
      upper curvatureLeft contraction *
    reggeWheelerSchwarzschildChristoffel
      frame contraction curvatureRight transported +
  reggeWheelerSchwarzschildChristoffel
      frame upper curvatureLeft contraction *
    connectionJet.connectionValue
      contraction curvatureRight transported -
  connectionJet.connectionValue
      upper curvatureRight contraction *
    reggeWheelerSchwarzschildChristoffel
      frame contraction curvatureLeft transported -
  reggeWheelerSchwarzschildChristoffel
      frame upper curvatureRight contraction *
    connectionJet.connectionValue
      contraction curvatureLeft transported

/--
The product-rule Riemann summand changes sign when the curvature indices are
exchanged.
-/
theorem
    reggeWheelerOddParityLinearizedRiemannSummand_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedRiemannSummand
        frame connectionJet upper transported
        curvatureLeft curvatureRight contraction =
      -reggeWheelerOddParityLinearizedRiemannSummand
        frame connectionJet upper transported
        curvatureRight curvatureLeft contraction := by
  unfold reggeWheelerOddParityLinearizedRiemannSummand
  ring

/--
Negation commutes with the explicit four-coordinate contraction.
-/
theorem reggeWheelerSpacetimeCoordinateContraction_neg
    (term : ReggeWheelerSpacetimeCoordinate → ℝ) :
    reggeWheelerSpacetimeCoordinateContraction
        (fun coordinate => -term coordinate) =
      -reggeWheelerSpacetimeCoordinateContraction term := by
  unfold reggeWheelerSpacetimeCoordinateContraction
  ring

/--
The complete mixed-index odd-parity linearized Riemann tensor:

`δR^ρ_{σμν}
  = ∂_μ δΓ^ρ_{νσ} - ∂_ν δΓ^ρ_{μσ}
    + δΓ^ρ_{μλ} Γ^λ_{νσ}
    + Γ^ρ_{μλ} δΓ^λ_{νσ}
    - δΓ^ρ_{νλ} Γ^λ_{μσ}
    - Γ^ρ_{νλ} δΓ^λ_{μσ}`.

The `λ` contraction is the explicit sum over the four Schwarzschild
coordinate labels.
-/
def reggeWheelerOddParityLinearizedRiemann
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  connectionJet.connectionPartial
      curvatureLeft upper curvatureRight transported -
    connectionJet.connectionPartial
      curvatureRight upper curvatureLeft transported +
    reggeWheelerSpacetimeCoordinateContraction
      (fun contraction =>
        reggeWheelerOddParityLinearizedRiemannSummand
          frame connectionJet upper transported
          curvatureLeft curvatureRight contraction)

/--
The complete linearized Riemann tensor is antisymmetric in its two curvature
indices.
-/
theorem
    reggeWheelerOddParityLinearizedRiemann_curvatureIndices_antisymmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (upper transported curvatureLeft curvatureRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedRiemann
        frame connectionJet upper transported
        curvatureLeft curvatureRight =
      -reggeWheelerOddParityLinearizedRiemann
        frame connectionJet upper transported
        curvatureRight curvatureLeft := by
  have hPointwise :
      ∀ contraction,
        reggeWheelerOddParityLinearizedRiemannSummand
            frame connectionJet upper transported
            curvatureLeft curvatureRight contraction =
          -reggeWheelerOddParityLinearizedRiemannSummand
            frame connectionJet upper transported
            curvatureRight curvatureLeft contraction := by
    intro contraction
    exact
      reggeWheelerOddParityLinearizedRiemannSummand_curvatureIndices_antisymmetric
        frame connectionJet upper transported
        curvatureLeft curvatureRight contraction

  have hContraction :
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedRiemannSummand
              frame connectionJet upper transported
              curvatureLeft curvatureRight contraction) =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedRiemannSummand
              frame connectionJet upper transported
              curvatureRight curvatureLeft contraction) := by
    calc
      reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedRiemannSummand
              frame connectionJet upper transported
              curvatureLeft curvatureRight contraction)
          =
        reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            -reggeWheelerOddParityLinearizedRiemannSummand
              frame connectionJet upper transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_congr
                (fun contraction =>
                  reggeWheelerOddParityLinearizedRiemannSummand
                    frame connectionJet upper transported
                    curvatureLeft curvatureRight contraction)
                (fun contraction =>
                  -reggeWheelerOddParityLinearizedRiemannSummand
                    frame connectionJet upper transported
                    curvatureRight curvatureLeft contraction)
                hPointwise
      _ =
        -reggeWheelerSpacetimeCoordinateContraction
          (fun contraction =>
            reggeWheelerOddParityLinearizedRiemannSummand
              frame connectionJet upper transported
              curvatureRight curvatureLeft contraction) := by
            exact
              reggeWheelerSpacetimeCoordinateContraction_neg
                (fun contraction =>
                  reggeWheelerOddParityLinearizedRiemannSummand
                    frame connectionJet upper transported
                    curvatureRight curvatureLeft contraction)

  unfold reggeWheelerOddParityLinearizedRiemann
  rw [hContraction]
  ring

/--
A linearized Riemann component with repeated curvature indices vanishes.
-/
theorem reggeWheelerOddParityLinearizedRiemann_curvatureDiagonal_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (connectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (upper transported curvature :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedRiemann
        frame connectionJet upper transported
        curvature curvature =
      0 := by
  have hAntisymmetric :=
    reggeWheelerOddParityLinearizedRiemann_curvatureIndices_antisymmetric
      frame connectionJet upper transported curvature curvature
  linarith

def reggeWheelerOddParityLinearizedRiemannBoundary : String :=
  "MIXED_INDEX_ODD_PARITY_LINEARIZED_RIEMANN_AND_CURVATURE_INDEX_ANTISYMMETRY_PROVED_CONNECTION_DERIVATIVES_REMAIN_SUPPLIED_DATA_LOWERED_RIEMANN_TIDAL_FRAME_PROJECTION_GEODESIC_DEVIATION_AND_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
