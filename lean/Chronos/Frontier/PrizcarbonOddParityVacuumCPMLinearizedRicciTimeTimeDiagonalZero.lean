import Chronos.Frontier.PrizcarbonOddParityVacuumCPMLinearizedRicciTimeTimeExpansion

namespace Chronos.Frontier

noncomputable section

/--
A mixed-index linearized Riemann component vanishes whenever its two curvature
indices coincide.

Only antisymmetry in the final curvature-index pair is used.
-/
theorem
    prizcarbonOddParityLinearizedRiemann_curvatureDiagonal_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (contraction transported curvature :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedRiemann
        frame
        linearizedConnectionJet
        contraction
        transported
        curvature
        curvature =
      0 := by
  have hAntisymmetric :=
    reggeWheelerOddParityLinearizedRiemann_curvatureIndices_antisymmetric
      frame
      linearizedConnectionJet
      contraction
      transported
      curvature
      curvature

  linarith

/--
The repeated-time mixed-index component appearing in the coordinate
vacuum-CPM time-time Ricci contraction vanishes.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRiemann_time_time_time_time_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedRiemann
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
            frame
            cpmJet
            harmonicJet
        )
        .time
        .time
        .time
        .time =
      0 := by
  exact
    prizcarbonOddParityLinearizedRiemann_curvatureDiagonal_zero
      frame
      (
        reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
          frame
          cpmJet
          harmonicJet
      )
      .time
      .time
      .time

/--
The fully lowered vacuum-CPM `tttt` linearized Riemann component also
vanishes. This is a direct specialization of the repository's existing
generic curvature-diagonal zero theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLoweredLinearizedRiemann_time_time_time_time_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
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
        .time
        .time
        .time
        .time =
      0 := by
  exact
    reggeWheelerOddParityLoweredLinearizedRiemann_curvatureDiagonal_zero
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
      .time
      .time
      .time

/--
After eliminating the repeated-time term, the coordinate vacuum-CPM
time-time linearized Ricci component consists of exactly three contracted
linearized-Riemann components.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_threeContractedRiemannCoordinates
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime
        frame
        cpmJet
        harmonicJet =
      reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .radial
          .time
          .radial
          .time +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .theta
          .time
          .theta
          .time +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .phi
          .time
          .phi
          .time := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_contractedRiemannCoordinates,
    prizcarbonOddParityVacuumCPMLinearizedRiemann_time_time_time_time_eq_zero,
    zero_add
  ]

/--
The time-weighted coordinate contribution inherits the corrected three-term
expansion.
-/
theorem
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution_eq_threeContractedRiemannCoordinates
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution
        frame
        cpmJet
        harmonicJet =
      -(1 /
          reggeWheelerSchwarzschildExteriorFactor
            frame.background) *
        (
          reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .radial
              .time
              .radial
              .time +
            reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .theta
              .time
              .theta
              .time +
            reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .phi
              .time
              .phi
              .time
        ) := by
  unfold
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_threeContractedRiemannCoordinates
  ]

def
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTimeDiagonalZeroBoundary :
    String :=
  "VACUUM_CPM_REPEATED_TIME_CURVATURE_ZERO_PROVED_COORDINATE_RICCI_TIME_TIME_REDUCED_TO_THREE_TERMS_STATIC_TETRAD_TRACE_BRIDGE_OPEN"

end

end Chronos.Frontier
