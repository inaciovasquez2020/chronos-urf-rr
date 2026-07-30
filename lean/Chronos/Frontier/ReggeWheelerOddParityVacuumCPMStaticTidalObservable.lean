import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricSecondJet
import Chronos.Frontier.ReggeWheelerOddParityStaticTidalProjection

namespace Chronos.Frontier

noncomputable section

/--
The coordinate derivative of the Schwarzschild Christoffel symbol.

The existing Schwarzschild connection is

`Γ̄^ρ_{μν}
  = 1/2 ḡ^{ρρ} K̄_{μνρ}`,

where

`K̄_{μνρ}
  = ∂_μ ḡ_{νρ}
    + ∂_ν ḡ_{μρ}
    - ∂_ρ ḡ_{μν}`.

This definition applies the product rule using the already explicit
derivative of the inverse Schwarzschild metric and the already explicit
derivative of the background connection kernel.
-/
def reggeWheelerSchwarzschildChristoffelPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) : ℝ :=
  (1 / 2 : ℝ) *
    (
      reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            derivative
            upper
            upper *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            lowerLeft
            lowerRight
            upper +

        reggeWheelerSchwarzschildInverseMetricDiagonal
            frame
            upper *
          reggeWheelerSchwarzschildConnectionKernelPartial
            frame
            derivative
            lowerLeft
            lowerRight
            upper
    )

/--
Construct the complete first coordinate jet of the background Schwarzschild
connection from the static Schwarzschild frame.

Unlike the earlier carrier constructor, this accepts no independently
supplied `connectionPartial` function.
-/
def reggeWheelerSchwarzschildConnectionFirstJetOfFrame
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    ReggeWheelerSchwarzschildConnectionFirstJet where
  connectionPartial :=
    reggeWheelerSchwarzschildChristoffelPartial frame

/--
The derivative field of the background connection first jet is exactly the
product-rule derivative of the explicit Schwarzschild Christoffel symbol.
-/
theorem
    reggeWheelerSchwarzschildConnectionFirstJetOfFrame_connectionPartial
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    (
      reggeWheelerSchwarzschildConnectionFirstJetOfFrame frame
    ).connectionPartial =
      reggeWheelerSchwarzschildChristoffelPartial frame := by
  rfl

/--
A component-level form of the background connection derivative
reconstruction.
-/
theorem
    reggeWheelerSchwarzschildConnectionFirstJetOfFrame_connectionPartial_apply
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerSchwarzschildConnectionFirstJetOfFrame frame
    ).connectionPartial
        derivative
        upper
        lowerLeft
        lowerRight =
      reggeWheelerSchwarzschildChristoffelPartial
        frame
        derivative
        upper
        lowerLeft
        lowerRight := by
  rfl

/--
The metric second jet derived from one vacuum CPM third jet and one
vector-harmonic coordinate second jet.
-/
def reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerOddParityMetricPerturbationSecondJet :=
  reggeWheelerOddParityVacuumCPMMetricSecondJet
    cpmJet
    harmonicJet

/--
The metric first jet contained in the derived metric second jet.
-/
def reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerOddParityMetricPerturbationFirstJet :=
  (
    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
      cpmJet
      harmonicJet
  ).firstJet

/--
The linearized-connection first jet obtained by differentiating the
metric-derived linearized Christoffel symbol.
-/
def reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerOddParityLinearizedConnectionFirstJet :=
  reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
    frame
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    )

/--
The complete local vacuum-CPM odd-parity static-frame tidal-curvature
observable.

Its inputs are:

* a certified static Schwarzschild frame;
* one vacuum CPM third jet;
* one vector-harmonic coordinate second jet;
* two detector spatial axes.

No independent perturbation metric jet, perturbation connection jet, or
background connection jet is supplied.
-/
def reggeWheelerOddParityVacuumCPMStaticTidalCurvature
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (left right : ReggeWheelerDetectorSpatialAxis) : ℝ :=
  reggeWheelerOddParityStaticTidalCurvature
    frame
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
        cpmJet
        harmonicJet
    )
    (
      reggeWheelerSchwarzschildConnectionFirstJetOfFrame
        frame
    )
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet
    )
    left
    right

/--
The complete CPM-derived static-frame tidal observable equals the associated
fully lowered linearized Riemann coordinate component multiplied by the four
explicit orthonormal-frame scale factors.
-/
theorem
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature_coordinateFormula
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (left right : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature
        frame
        cpmJet
        harmonicJet
        left
        right =
      reggeWheelerOddParityLoweredLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
              cpmJet
              harmonicJet
          )
          (
            reggeWheelerSchwarzschildConnectionFirstJetOfFrame
              frame
          )
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          (reggeWheelerDetectorSpatialCoordinate left)
          .time
          (reggeWheelerDetectorSpatialCoordinate right)
          .time *
        reggeWheelerSchwarzschildStaticSpatialLegScale
          frame
          left *
        (1 / frame.lapseSqrt) *
        reggeWheelerSchwarzschildStaticSpatialLegScale
          frame
          right *
        (1 / frame.lapseSqrt) := by
  unfold reggeWheelerOddParityVacuumCPMStaticTidalCurvature
  exact
    reggeWheelerOddParityStaticTidalCurvature_coordinateFormula
      frame
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
          cpmJet
          harmonicJet
      )
      (
        reggeWheelerSchwarzschildConnectionFirstJetOfFrame
          frame
      )
      (
        reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
          frame
          cpmJet
          harmonicJet
      )
      left
      right

/--
The complete local observable uses exactly the CPM-derived metric first jet.
-/
theorem
    reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet_eq
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
        cpmJet
        harmonicJet =
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        cpmJet.secondJet
        harmonicJet.firstJet := by
  rfl

/--
The complete local observable uses exactly the product-rule-derived
linearized connection first jet.
-/
theorem
    reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet_eq
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet =
      reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
        frame
        (
          reggeWheelerOddParityVacuumCPMMetricSecondJet
            cpmJet
            harmonicJet
        ) := by
  rfl

def reggeWheelerOddParityVacuumCPMStaticTidalObservableBoundary :
    String :=
  "COMPLETE_LOCAL_VACUUM_CPM_TO_STATIC_ORTHONORMAL_FRAME_TIDAL_CURVATURE_CHAIN_CONSTRUCTED_WITHOUT_SUPPLIED_METRIC_FIRST_JET_METRIC_SECOND_JET_LINEARIZED_CONNECTION_FIRST_JET_OR_BACKGROUND_CONNECTION_FIRST_JET_CPM_THIRD_DERIVATIVES_AND_ANGULAR_HARMONIC_SECOND_DERIVATIVES_REMAIN_LOCAL_SUPPLIED_DATA_STATIC_FRAME_IS_ACCELERATED_NOT_FREE_FALL_TIDAL_MATRIX_SYMMETRY_GEODESIC_DEVIATION_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
