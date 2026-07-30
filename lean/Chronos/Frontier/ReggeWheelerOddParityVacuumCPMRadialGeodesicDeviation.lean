import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMStaticTidalObservable

namespace Chronos.Frontier

noncomputable section

/--
Pointwise radial timelike-geodesic first-integral data in the Schwarzschild
exterior.

The fields encode the local first integral

`(uʳ)² + f(r) = E²`

for an ingoing radial observer. This is local tangent-frame data. It does not
by itself construct a worldline or prove the differential geodesic equation
along an interval.
-/
structure ReggeWheelerSchwarzschildRadialGeodesicPointData where
  frame : ReggeWheelerSchwarzschildStaticDetectorFrame
  energy : ℝ
  radialSpeed : ℝ
  energy_pos : 0 < energy
  radialSpeed_nonneg : 0 ≤ radialSpeed
  radialFirstIntegral :
    radialSpeed ^ 2 +
        reggeWheelerSchwarzschildExteriorFactor frame.background =
      energy ^ 2

/--
Canonical ingoing radial-geodesic point data for an allowed conserved energy.

The radial speed is

`√(E² - f(r))`.
-/
def reggeWheelerSchwarzschildRadialGeodesicPointDataCanonical
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (energy : ℝ)
    (energy_pos : 0 < energy)
    (factor_le_energy_sq :
      reggeWheelerSchwarzschildExteriorFactor frame.background ≤
        energy ^ 2) :
    ReggeWheelerSchwarzschildRadialGeodesicPointData where
  frame := frame
  energy := energy
  radialSpeed :=
    Real.sqrt
      (
        energy ^ 2 -
          reggeWheelerSchwarzschildExteriorFactor frame.background
      )
  energy_pos := energy_pos
  radialSpeed_nonneg :=
    Real.sqrt_nonneg
      (
        energy ^ 2 -
          reggeWheelerSchwarzschildExteriorFactor frame.background
      )
  radialFirstIntegral := by
    have speed_sq :
        (
          Real.sqrt
            (
              energy ^ 2 -
                reggeWheelerSchwarzschildExteriorFactor frame.background
            )
        ) ^ 2 =
          energy ^ 2 -
            reggeWheelerSchwarzschildExteriorFactor frame.background :=
      Real.sq_sqrt
        (
          sub_nonneg.mpr factor_le_energy_sq
        )
    nlinarith

/--
The future-directed ingoing radial four-velocity

`u = (E/f) ∂ₜ - v ∂ᵣ`.
-/
def reggeWheelerSchwarzschildRadialGeodesicTimeLeg
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    ReggeWheelerSpacetimeVectorValue
  | .time =>
      data.energy /
        reggeWheelerSchwarzschildExteriorFactor data.frame.background
  | .radial =>
      -data.radialSpeed
  | .theta =>
      0
  | .phi =>
      0

/--
The unit radial spatial leg orthogonal to the radial-geodesic time leg:

`e_(1) = -(v/f) ∂ₜ + E ∂ᵣ`.
-/
def reggeWheelerSchwarzschildRadialGeodesicRadialLeg
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    ReggeWheelerSpacetimeVectorValue
  | .time =>
      -data.radialSpeed /
        reggeWheelerSchwarzschildExteriorFactor data.frame.background
  | .radial =>
      data.energy
  | .theta =>
      0
  | .phi =>
      0

/--
The angular legs are inherited from the already certified Schwarzschild
orthonormal frame.
-/
def reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    ReggeWheelerDetectorSpatialAxis →
      ReggeWheelerSpacetimeVectorValue
  | .radial =>
      reggeWheelerSchwarzschildRadialGeodesicRadialLeg data
  | .theta =>
      reggeWheelerSchwarzschildStaticThetaLeg data.frame
  | .phi =>
      reggeWheelerSchwarzschildStaticPhiLeg data.frame

private theorem radialGeodesicTimelikeAlgebra
    (factor energy speed : ℝ)
    (factor_ne_zero : factor ≠ 0)
    (firstIntegral : speed ^ 2 + factor = energy ^ 2) :
    -factor *
          (energy / factor) *
          (energy / factor) +
        (1 / factor) *
          (-speed) *
          (-speed) =
      -1 := by
  field_simp [factor_ne_zero]
  nlinarith

private theorem radialGeodesicRadialUnitAlgebra
    (factor energy speed : ℝ)
    (factor_ne_zero : factor ≠ 0)
    (firstIntegral : speed ^ 2 + factor = energy ^ 2) :
    -factor *
          (-speed / factor) *
          (-speed / factor) +
        (1 / factor) *
          energy *
          energy =
      1 := by
  field_simp [factor_ne_zero]
  nlinarith

private theorem radialGeodesicOrthogonalAlgebra
    (factor energy speed : ℝ)
    (factor_ne_zero : factor ≠ 0) :
    -factor *
          (energy / factor) *
          (-speed / factor) +
        (1 / factor) *
          (-speed) *
          energy =
      0 := by
  field_simp [factor_ne_zero]
  ring

/--
The radial-geodesic four-velocity is unit timelike in signature `(-,+,+,+)`.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimeLeg_unitTimelike
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicTimeLeg data)
        (reggeWheelerSchwarzschildRadialGeodesicTimeLeg data) =
      -1 := by
  have factor_ne_zero :
      reggeWheelerSchwarzschildExteriorFactor
          data.frame.background ≠ 0 :=
    reggeWheelerSchwarzschildExteriorFactor_ne_zero
      data.frame.background
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg
  ] using
    radialGeodesicTimelikeAlgebra
      (reggeWheelerSchwarzschildExteriorFactor data.frame.background)
      data.energy
      data.radialSpeed
      factor_ne_zero
      data.radialFirstIntegral

/--
The boosted radial spatial leg has unit positive norm.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicRadialLeg_unitSpacelike
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicRadialLeg data)
        (reggeWheelerSchwarzschildRadialGeodesicRadialLeg data) =
      1 := by
  have factor_ne_zero :
      reggeWheelerSchwarzschildExteriorFactor
          data.frame.background ≠ 0 :=
    reggeWheelerSchwarzschildExteriorFactor_ne_zero
      data.frame.background
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicRadialLeg
  ] using
    radialGeodesicRadialUnitAlgebra
      (reggeWheelerSchwarzschildExteriorFactor data.frame.background)
      data.energy
      data.radialSpeed
      factor_ne_zero
      data.radialFirstIntegral

/--
The radial-geodesic time leg and radial spatial leg are orthogonal.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimeRadial_orthogonal
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicTimeLeg data)
        (reggeWheelerSchwarzschildRadialGeodesicRadialLeg data) =
      0 := by
  have factor_ne_zero :
      reggeWheelerSchwarzschildExteriorFactor
          data.frame.background ≠ 0 :=
    reggeWheelerSchwarzschildExteriorFactor_ne_zero
      data.frame.background
  simpa [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg,
    reggeWheelerSchwarzschildRadialGeodesicRadialLeg
  ] using
    radialGeodesicOrthogonalAlgebra
      (reggeWheelerSchwarzschildExteriorFactor data.frame.background)
      data.energy
      data.radialSpeed
      factor_ne_zero

/--
The radial-geodesic time leg is future directed.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimeLeg_timeComponent_pos
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    0 <
      reggeWheelerSchwarzschildRadialGeodesicTimeLeg data .time := by
  simp only [
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg
  ]
  exact
    div_pos
      data.energy_pos
      (
        reggeWheelerSchwarzschildExteriorFactor_pos
          data.frame.background
      )

/--
The radial component of the chosen ingoing four-velocity is nonpositive.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimeLeg_radialComponent_nonpos
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg data .radial ≤ 0 := by
  simp only [
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg
  ]
  linarith [data.radialSpeed_nonneg]

/--
The radial-geodesic time leg is orthogonal to the unchanged theta leg.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimeTheta_orthogonal
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicTimeLeg data)
        (reggeWheelerSchwarzschildStaticThetaLeg data.frame) =
      0 := by
  simp [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg,
    reggeWheelerSchwarzschildStaticThetaLeg
  ]

/--
The radial-geodesic time leg is orthogonal to the unchanged phi leg.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicTimePhi_orthogonal
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicTimeLeg data)
        (reggeWheelerSchwarzschildStaticPhiLeg data.frame) =
      0 := by
  simp [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicTimeLeg,
    reggeWheelerSchwarzschildStaticPhiLeg
  ]

/--
The boosted radial leg is orthogonal to the unchanged theta leg.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicRadialTheta_orthogonal
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicRadialLeg data)
        (reggeWheelerSchwarzschildStaticThetaLeg data.frame) =
      0 := by
  simp [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicRadialLeg,
    reggeWheelerSchwarzschildStaticThetaLeg
  ]

/--
The boosted radial leg is orthogonal to the unchanged phi leg.
-/
theorem reggeWheelerSchwarzschildRadialGeodesicRadialPhi_orthogonal
    (data : ReggeWheelerSchwarzschildRadialGeodesicPointData) :
    reggeWheelerSchwarzschildMetricPair
        data.frame
        (reggeWheelerSchwarzschildRadialGeodesicRadialLeg data)
        (reggeWheelerSchwarzschildStaticPhiLeg data.frame) =
      0 := by
  simp [
    reggeWheelerSchwarzschildMetricPair,
    reggeWheelerSchwarzschildRadialGeodesicRadialLeg,
    reggeWheelerSchwarzschildStaticPhiLeg
  ]

/--
The complete CPM-derived fully lowered linearized Riemann tensor used by the
radial-geodesic observer.
-/
def reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ :=
  reggeWheelerOddParityLoweredLinearizedRiemann
    observer.frame
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
        cpmJet
        harmonicJet
    )
    (
      reggeWheelerSchwarzschildConnectionFirstJetOfFrame
        observer.frame
    )
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        observer.frame
        cpmJet
        harmonicJet
    )

/--
The odd-parity tidal-curvature matrix seen in the local radial-geodesic
tetrad:

`𝓔_ab = δR_{αβγδ} e_a^α u^β e_b^γ u^δ`.

No sign is inserted in this curvature projection.
-/
def reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (left right : ReggeWheelerDetectorSpatialAxis) : ℝ :=
  reggeWheelerSpacetimeRankFourProjection
    (
      reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
        observer
        cpmJet
        harmonicJet
    )
    (
      reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
        observer
        left
    )
    (
      reggeWheelerSchwarzschildRadialGeodesicTimeLeg
        observer
    )
    (
      reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
        observer
        right
    )
    (
      reggeWheelerSchwarzschildRadialGeodesicTimeLeg
        observer
    )

/--
The radial-geodesic tidal observable is exactly the four-leg projection of
the complete CPM-derived lowered linearized Riemann tensor.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature_eq_projection
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (left right : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
        observer
        cpmJet
        harmonicJet
        left
        right =
      reggeWheelerSpacetimeRankFourProjection
        (
          reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
            observer
            cpmJet
            harmonicJet
        )
        (
          reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
            observer
            left
        )
        (
          reggeWheelerSchwarzschildRadialGeodesicTimeLeg
            observer
        )
        (
          reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
            observer
            right
        )
        (
          reggeWheelerSchwarzschildRadialGeodesicTimeLeg
            observer
        ) := by
  rfl

/--
Finite contraction over the three detector spatial axes.
-/
def reggeWheelerDetectorSpatialContraction
    (component : ReggeWheelerDetectorSpatialAxis → ℝ) : ℝ :=
  component .radial +
    component .theta +
    component .phi

/--
Pointwise first-order relative acceleration under the explicit convention

`D²ξ^α/dτ² = -R^α_{ βγδ} u^β ξ^γ u^δ`.

In the orthonormal detector frame this is

`a_a = -Σ_b 𝓔_ab ξ_b`.
-/
def reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (separation :
      ReggeWheelerDetectorSpatialAxis → ℝ)
    (outputAxis : ReggeWheelerDetectorSpatialAxis) : ℝ :=
  -reggeWheelerDetectorSpatialContraction
    (
      fun inputAxis =>
        reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
            observer
            cpmJet
            harmonicJet
            outputAxis
            inputAxis *
          separation inputAxis
    )

/--
The pointwise relative acceleration is the negative tidal-matrix contraction
with the spatial separation vector.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration_eq_negativeTidalContraction
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (separation :
      ReggeWheelerDetectorSpatialAxis → ℝ)
    (outputAxis : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration
        observer
        cpmJet
        harmonicJet
        separation
        outputAxis =
      -(
        reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
              observer
              cpmJet
              harmonicJet
              outputAxis
              .radial *
            separation .radial +

          reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
              observer
              cpmJet
              harmonicJet
              outputAxis
              .theta *
            separation .theta +

          reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
              observer
              cpmJet
              harmonicJet
              outputAxis
              .phi *
            separation .phi
      ) := by
  rfl

/--
Zero separation produces zero pointwise relative acceleration.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration_zeroSeparation
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (outputAxis : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration
        observer
        cpmJet
        harmonicJet
        (fun _ => 0)
        outputAxis =
      0 := by
  simp [
    reggeWheelerOddParityVacuumCPMRadialGeodesicRelativeAcceleration,
    reggeWheelerDetectorSpatialContraction
  ]

def reggeWheelerOddParityVacuumCPMRadialGeodesicDeviationBoundary :
    String :=
  "POINTWISE_RADIAL_TIMELIKE_GEODESIC_FIRST_INTEGRAL_DATA_NOW_GIVES_A_FUTURE_DIRECTED_UNIT_TIMELIKE_LEG_AN_ORTHOGONAL_UNIT_RADIAL_LEG_A_COMPLETE_CPM_DERIVED_FREE_FALL_FRAME_CURVATURE_PROJECTION_AND_THE_EXPLICIT_RELATIVE_ACCELERATION_CONVENTION_A_EQUALS_MINUS_TIDAL_MATRIX_TIMES_SEPARATION_GLOBAL_WORLDLINE_EXISTENCE_THE_DIFFERENTIAL_GEODESIC_EQUATION_FRAME_TRANSPORT_TIDAL_MATRIX_SYMMETRY_CPM_WAVE_DERIVATION_AND_INTEGRATED_PHYSICAL_STRAIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
