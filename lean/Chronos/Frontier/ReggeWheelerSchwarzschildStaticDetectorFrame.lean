import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityMasterExtraction

namespace Chronos.Frontier

noncomputable section

/-- A pointwise vector in the local Schwarzschild coordinate chart. -/
abbrev ReggeWheelerSpacetimeVectorValue :=
  ReggeWheelerSpacetimeCoordinate → ℝ

/--
A certified stationary orthonormal-frame location in the Schwarzschild
exterior.

This is a stationary local frame, not a freely falling geodesic worldline.
-/
structure ReggeWheelerSchwarzschildStaticDetectorFrame where
  background : ReggeWheelerSchwarzschildBackground
  polarAngle : ℝ
  sinPolarAngle_ne_zero : Real.sin polarAngle ≠ 0
  lapseSqrt : ℝ
  lapseSqrt_pos : 0 < lapseSqrt
  lapseSqrt_sq :
    lapseSqrt ^ 2 =
      reggeWheelerSchwarzschildExteriorFactor background

/-- Canonical frame using the positive square root of the exterior factor. -/
def reggeWheelerSchwarzschildStaticDetectorFrameCanonical
    (background : ReggeWheelerSchwarzschildBackground)
    (polarAngle : ℝ)
    (sinPolarAngle_ne_zero : Real.sin polarAngle ≠ 0) :
    ReggeWheelerSchwarzschildStaticDetectorFrame where
  background := background
  polarAngle := polarAngle
  sinPolarAngle_ne_zero := sinPolarAngle_ne_zero
  lapseSqrt :=
    Real.sqrt
      (reggeWheelerSchwarzschildExteriorFactor background)
  lapseSqrt_pos :=
    Real.sqrt_pos.2
      (reggeWheelerSchwarzschildExteriorFactor_pos background)
  lapseSqrt_sq :=
    Real.sq_sqrt
      (le_of_lt
        (reggeWheelerSchwarzschildExteriorFactor_pos background))

/--
Schwarzschild coordinate-metric pairing with signature `(-,+,+,+)`.
-/
def reggeWheelerSchwarzschildMetricPair
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (left right : ReggeWheelerSpacetimeVectorValue) : ℝ :=
  -(reggeWheelerSchwarzschildExteriorFactor frame.background) *
        left .time * right .time +
    (1 /
        reggeWheelerSchwarzschildExteriorFactor frame.background) *
        left .radial * right .radial +
    frame.background.radius ^ 2 *
        left .theta * right .theta +
    (frame.background.radius *
        Real.sin frame.polarAngle) ^ 2 *
        left .phi * right .phi

theorem reggeWheelerSchwarzschildMetricPair_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (left right : ReggeWheelerSpacetimeVectorValue) :
    reggeWheelerSchwarzschildMetricPair frame left right =
      reggeWheelerSchwarzschildMetricPair frame right left := by
  unfold reggeWheelerSchwarzschildMetricPair
  ring

/-- `e_(0) = f⁻¹ᐟ² ∂_t`. -/
def reggeWheelerSchwarzschildStaticTimeLeg
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeVectorValue
  | .time => 1 / frame.lapseSqrt
  | _ => 0

/-- `e_(1) = f¹ᐟ² ∂_r`. -/
def reggeWheelerSchwarzschildStaticRadialLeg
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeVectorValue
  | .radial => frame.lapseSqrt
  | _ => 0

/-- `e_(2) = r⁻¹ ∂_θ`. -/
def reggeWheelerSchwarzschildStaticThetaLeg
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeVectorValue
  | .theta => 1 / frame.background.radius
  | _ => 0

/-- `e_(3) = (r sin θ)⁻¹ ∂_φ`. -/
def reggeWheelerSchwarzschildStaticPhiLeg
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSpacetimeVectorValue
  | .phi =>
      1 /
        (frame.background.radius *
          Real.sin frame.polarAngle)
  | _ => 0

private theorem square_reciprocal_cancel
    (value : ℝ)
    (value_ne_zero : value ≠ 0) :
    value ^ 2 * (1 / value) * (1 / value) = 1 := by
  field_simp

private theorem negative_square_reciprocal_cancel
    (value : ℝ)
    (value_ne_zero : value ≠ 0) :
    -(value ^ 2) * (1 / value) * (1 / value) = -1 := by
  field_simp

private theorem reciprocal_square_cancel
    (value : ℝ)
    (value_ne_zero : value ≠ 0) :
    (1 / value ^ 2) * value * value = 1 := by
  field_simp

theorem reggeWheelerSchwarzschildStaticTimeLeg_norm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticTimeLeg frame)
        (reggeWheelerSchwarzschildStaticTimeLeg frame) =
      -1 := by
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildStaticTimeLeg,
    ← frame.lapseSqrt_sq
  ] using
    negative_square_reciprocal_cancel
      frame.lapseSqrt
      (ne_of_gt frame.lapseSqrt_pos)

theorem reggeWheelerSchwarzschildStaticRadialLeg_norm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticRadialLeg frame)
        (reggeWheelerSchwarzschildStaticRadialLeg frame) =
      1 := by
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildStaticRadialLeg,
    ← frame.lapseSqrt_sq
  ] using
    reciprocal_square_cancel
      frame.lapseSqrt
      (ne_of_gt frame.lapseSqrt_pos)

theorem reggeWheelerSchwarzschildStaticThetaLeg_norm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticThetaLeg frame)
        (reggeWheelerSchwarzschildStaticThetaLeg frame) =
      1 := by
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildStaticThetaLeg
  ] using
    square_reciprocal_cancel
      frame.background.radius
      (ne_of_gt
        (reggeWheelerSchwarzschildBackground_radius_pos
          frame.background))

theorem reggeWheelerSchwarzschildStaticPhiLeg_norm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticPhiLeg frame)
        (reggeWheelerSchwarzschildStaticPhiLeg frame) =
      1 := by
  have hRadius :
      frame.background.radius ≠ 0 :=
    ne_of_gt
      (reggeWheelerSchwarzschildBackground_radius_pos
        frame.background)
  have hProduct :
      frame.background.radius *
          Real.sin frame.polarAngle ≠ 0 :=
    mul_ne_zero hRadius frame.sinPolarAngle_ne_zero
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildStaticPhiLeg
  ] using
    square_reciprocal_cancel
      (frame.background.radius *
        Real.sin frame.polarAngle)
      hProduct

/-- All distinct static-frame legs are mutually orthogonal. -/
theorem
    reggeWheelerSchwarzschildStaticDetectorFrame_pairwiseOrthogonal
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticTimeLeg frame)
        (reggeWheelerSchwarzschildStaticRadialLeg frame) = 0 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticTimeLeg frame)
        (reggeWheelerSchwarzschildStaticThetaLeg frame) = 0 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticTimeLeg frame)
        (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticRadialLeg frame)
        (reggeWheelerSchwarzschildStaticThetaLeg frame) = 0 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticRadialLeg frame)
        (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticThetaLeg frame)
        (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0 := by
  simp [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildStaticTimeLeg,
    reggeWheelerSchwarzschildStaticRadialLeg,
    reggeWheelerSchwarzschildStaticThetaLeg,
    reggeWheelerSchwarzschildStaticPhiLeg
  ]

/--
The static Schwarzschild frame is orthonormal with signature `(-,+,+,+)`.
-/
theorem reggeWheelerSchwarzschildStaticDetectorFrame_orthonormal
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticTimeLeg frame)
        (reggeWheelerSchwarzschildStaticTimeLeg frame) = -1 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticRadialLeg frame)
        (reggeWheelerSchwarzschildStaticRadialLeg frame) = 1 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticThetaLeg frame)
        (reggeWheelerSchwarzschildStaticThetaLeg frame) = 1 ∧
    reggeWheelerSchwarzschildMetricPair frame
        (reggeWheelerSchwarzschildStaticPhiLeg frame)
        (reggeWheelerSchwarzschildStaticPhiLeg frame) = 1 ∧
    (
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticTimeLeg frame)
          (reggeWheelerSchwarzschildStaticRadialLeg frame) = 0 ∧
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticTimeLeg frame)
          (reggeWheelerSchwarzschildStaticThetaLeg frame) = 0 ∧
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticTimeLeg frame)
          (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0 ∧
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticRadialLeg frame)
          (reggeWheelerSchwarzschildStaticThetaLeg frame) = 0 ∧
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticRadialLeg frame)
          (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0 ∧
      reggeWheelerSchwarzschildMetricPair frame
          (reggeWheelerSchwarzschildStaticThetaLeg frame)
          (reggeWheelerSchwarzschildStaticPhiLeg frame) = 0
    ) := by
  exact ⟨
    reggeWheelerSchwarzschildStaticTimeLeg_norm frame,
    reggeWheelerSchwarzschildStaticRadialLeg_norm frame,
    reggeWheelerSchwarzschildStaticThetaLeg_norm frame,
    reggeWheelerSchwarzschildStaticPhiLeg_norm frame,
    reggeWheelerSchwarzschildStaticDetectorFrame_pairwiseOrthogonal
      frame
  ⟩

def reggeWheelerSchwarzschildStaticDetectorFrameBoundary : String :=
  "STATIC_SCHWARZSCHILD_COORDINATE_METRIC_AND_ORTHONORMAL_FRAME_PROVED_STATIONARY_FRAME_NOT_FREE_FALL_WORLDLINE_CONNECTION_CURVATURE_GEODESIC_DEVIATION_AND_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
