import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityLoweredLinearizedRiemann

namespace Chronos.Frontier

noncomputable section

/--
The three spatial axes of the local static Schwarzschild frame.
-/
inductive ReggeWheelerDetectorSpatialAxis
  | radial
  | theta
  | phi
  deriving DecidableEq

/--
The coordinate direction associated with each detector-frame spatial axis.
-/
def reggeWheelerDetectorSpatialCoordinate :
    ReggeWheelerDetectorSpatialAxis →
      ReggeWheelerSpacetimeCoordinate
  | .radial => .radial
  | .theta => .theta
  | .phi => .phi

/--
The coordinate scale of each static orthonormal spatial leg.
-/
def reggeWheelerSchwarzschildStaticSpatialLegScale
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerDetectorSpatialAxis → ℝ
  | .radial =>
      frame.lapseSqrt
  | .theta =>
      1 / frame.background.radius
  | .phi =>
      1 /
        (
          frame.background.radius *
            Real.sin frame.polarAngle
        )

/--
Select one of the three proved static orthonormal spatial legs.
-/
def reggeWheelerSchwarzschildStaticSpatialLeg
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerDetectorSpatialAxis →
      ReggeWheelerSpacetimeVectorValue
  | .radial =>
      reggeWheelerSchwarzschildStaticRadialLeg frame
  | .theta =>
      reggeWheelerSchwarzschildStaticThetaLeg frame
  | .phi =>
      reggeWheelerSchwarzschildStaticPhiLeg frame

/--
A scaled coordinate-basis vector.
-/
def reggeWheelerScaledCoordinateBasisVector
    (selected : ReggeWheelerSpacetimeCoordinate)
    (scale : ℝ) :
    ReggeWheelerSpacetimeVectorValue
  | coordinate =>
      if coordinate = selected then scale else 0

/--
The static timelike leg is `f⁻¹ᐟ² ∂ₜ`.
-/
theorem
    reggeWheelerSchwarzschildStaticTimeLeg_eq_scaledCoordinateBasis
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildStaticTimeLeg frame =
      reggeWheelerScaledCoordinateBasisVector
        .time
        (1 / frame.lapseSqrt) := by
  funext coordinate
  cases coordinate <;>
    rfl

/--
Every static spatial leg is a scaled coordinate-basis vector.
-/
theorem
    reggeWheelerSchwarzschildStaticSpatialLeg_eq_scaledCoordinateBasis
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (axis : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerSchwarzschildStaticSpatialLeg frame axis =
      reggeWheelerScaledCoordinateBasisVector
        (reggeWheelerDetectorSpatialCoordinate axis)
        (reggeWheelerSchwarzschildStaticSpatialLegScale
          frame axis) := by
  cases axis <;>
    funext coordinate <;>
      cases coordinate <;>
        rfl

/--
Contract one coordinate index against a spacetime vector.
-/
def reggeWheelerSpacetimeVectorContraction
    (term : ReggeWheelerSpacetimeCoordinate → ℝ)
    (vector : ReggeWheelerSpacetimeVectorValue) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun coordinate =>
      term coordinate * vector coordinate)

/--
Contracting against a scaled coordinate-basis vector selects one coordinate
component and multiplies it by the supplied scale.

This four-case result replaces the previous 256-case rank-four proof.
-/
theorem
    reggeWheelerSpacetimeVectorContraction_scaledCoordinateBasis
    (term : ReggeWheelerSpacetimeCoordinate → ℝ)
    (selected : ReggeWheelerSpacetimeCoordinate)
    (scale : ℝ) :
    reggeWheelerSpacetimeVectorContraction
        term
        (reggeWheelerScaledCoordinateBasisVector
          selected scale) =
      term selected * scale := by
  cases selected <;>
    simp [
      reggeWheelerSpacetimeVectorContraction,
      reggeWheelerSpacetimeCoordinateContraction,
      reggeWheelerScaledCoordinateBasisVector
    ]

/--
Contract a covariant rank-four coordinate tensor against four spacetime
vectors.
-/
def reggeWheelerSpacetimeRankFourProjection
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ)
    (first second third fourth :
      ReggeWheelerSpacetimeVectorValue) : ℝ :=
  reggeWheelerSpacetimeVectorContraction
    (fun firstIndex =>
      reggeWheelerSpacetimeVectorContraction
        (fun secondIndex =>
          reggeWheelerSpacetimeVectorContraction
            (fun thirdIndex =>
              reggeWheelerSpacetimeVectorContraction
                (fun fourthIndex =>
                  tensor
                    firstIndex
                    secondIndex
                    thirdIndex
                    fourthIndex)
                fourth)
            third)
        second)
    first

/--
Projection against four scaled coordinate-basis vectors selects exactly one
rank-four coordinate component.

The proof performs four one-index selections rather than expanding all
`4⁴ = 256` coordinate combinations.
-/
theorem
    reggeWheelerSpacetimeRankFourProjection_scaledCoordinateBasis
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ)
    (firstCoordinate secondCoordinate
      thirdCoordinate fourthCoordinate :
        ReggeWheelerSpacetimeCoordinate)
    (firstScale secondScale thirdScale fourthScale : ℝ) :
    reggeWheelerSpacetimeRankFourProjection
        tensor
        (reggeWheelerScaledCoordinateBasisVector
          firstCoordinate firstScale)
        (reggeWheelerScaledCoordinateBasisVector
          secondCoordinate secondScale)
        (reggeWheelerScaledCoordinateBasisVector
          thirdCoordinate thirdScale)
        (reggeWheelerScaledCoordinateBasisVector
          fourthCoordinate fourthScale) =
      tensor
          firstCoordinate
          secondCoordinate
          thirdCoordinate
          fourthCoordinate *
        firstScale *
        secondScale *
        thirdScale *
        fourthScale := by
  unfold reggeWheelerSpacetimeRankFourProjection
  simp only [
    reggeWheelerSpacetimeVectorContraction_scaledCoordinateBasis
  ]
  ring

/--
The static-frame odd-parity tidal-curvature component

`𝓔_ab = δR_{αβγδ} e_(a)^α u^β e_(b)^γ u^δ`.

No extra sign is inserted here. A later geodesic-deviation theorem must state
its curvature convention explicitly.
-/
def reggeWheelerOddParityStaticTidalCurvature
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (left right : ReggeWheelerDetectorSpatialAxis) : ℝ :=
  reggeWheelerSpacetimeRankFourProjection
    (reggeWheelerOddParityLoweredLinearizedRiemann
      frame
      metricJet
      backgroundConnectionJet
      linearizedConnectionJet)
    (reggeWheelerSchwarzschildStaticSpatialLeg frame left)
    (reggeWheelerSchwarzschildStaticTimeLeg frame)
    (reggeWheelerSchwarzschildStaticSpatialLeg frame right)
    (reggeWheelerSchwarzschildStaticTimeLeg frame)

/--
The detector-frame tidal-curvature component equals the associated coordinate
Riemann component multiplied by the four explicit frame scales.
-/
theorem reggeWheelerOddParityStaticTidalCurvature_coordinateFormula
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (metricJet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (backgroundConnectionJet :
      ReggeWheelerSchwarzschildConnectionFirstJet)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (left right : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityStaticTidalCurvature
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet
        left
        right =
      reggeWheelerOddParityLoweredLinearizedRiemann
          frame
          metricJet
          backgroundConnectionJet
          linearizedConnectionJet
          (reggeWheelerDetectorSpatialCoordinate left)
          .time
          (reggeWheelerDetectorSpatialCoordinate right)
          .time *
        reggeWheelerSchwarzschildStaticSpatialLegScale
          frame left *
        (1 / frame.lapseSqrt) *
        reggeWheelerSchwarzschildStaticSpatialLegScale
          frame right *
        (1 / frame.lapseSqrt) := by
  unfold reggeWheelerOddParityStaticTidalCurvature
  simpa only [
    reggeWheelerSchwarzschildStaticSpatialLeg_eq_scaledCoordinateBasis,
    reggeWheelerSchwarzschildStaticTimeLeg_eq_scaledCoordinateBasis
  ] using
    reggeWheelerSpacetimeRankFourProjection_scaledCoordinateBasis
      (reggeWheelerOddParityLoweredLinearizedRiemann
        frame
        metricJet
        backgroundConnectionJet
        linearizedConnectionJet)
      (reggeWheelerDetectorSpatialCoordinate left)
      .time
      (reggeWheelerDetectorSpatialCoordinate right)
      .time
      (reggeWheelerSchwarzschildStaticSpatialLegScale frame left)
      (1 / frame.lapseSqrt)
      (reggeWheelerSchwarzschildStaticSpatialLegScale frame right)
      (1 / frame.lapseSqrt)

def reggeWheelerOddParityStaticTidalProjectionBoundary : String :=
  "STATIC_ORTHONORMAL_FRAME_TIDAL_CURVATURE_PROJECTION_AND_EXACT_COORDINATE_SCALE_FORMULA_PROVED_TIDAL_MATRIX_SYMMETRY_REQUIRES_ADDITIONAL_LOWERED_RIEMANN_PAIR_SYMMETRY_STATIC_FRAME_IS_NOT_FREE_FALL_CONNECTION_JETS_REMAIN_SUPPLIED_DATA_GEODESIC_DEVIATION_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
