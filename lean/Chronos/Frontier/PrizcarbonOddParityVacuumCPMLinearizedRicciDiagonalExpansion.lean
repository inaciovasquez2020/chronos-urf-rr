import Chronos.Frontier.PrizcarbonSchwarzschildRicciContractionZero

namespace Chronos.Frontier

noncomputable section

/--
The remaining vacuum-CPM background-metric/linearized-Ricci contraction is
exactly the sum of its four diagonal Schwarzschild inverse-metric components.

Every off-diagonal term vanishes because the Schwarzschild inverse metric used
by the contraction is diagonal.
-/
theorem
    prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution_eq_diagonal
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution
        frame
        cpmJet
        harmonicJet =
      -(1 /
          reggeWheelerSchwarzschildExteriorFactor
            frame.background) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .time
            .time +
        reggeWheelerSchwarzschildExteriorFactor
            frame.background *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .radial
            .radial +
        (1 / frame.background.radius ^ 2) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .theta
            .theta +
        (1 /
            (
              frame.background.radius *
                Real.sin frame.polarAngle
            ) ^ 2) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .phi
            .phi := by
  simp [
    prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution,
    prizcarbonOddParityBackgroundMetricLinearizedRicciContribution,
    reggeWheelerSpacetimeCoordinateContraction,
    reggeWheelerSchwarzschildInverseMetricComponent,
    reggeWheelerSchwarzschildInverseMetricDiagonal
  ]

/--
After the previously proved elimination of the background-Ricci contribution,
the full vacuum-CPM scalar-curvature first variation has the same explicit
four-component diagonal form.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_diagonalLinearizedRicci
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
        frame
        cpmJet
        harmonicJet =
      -(1 /
          reggeWheelerSchwarzschildExteriorFactor
            frame.background) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .time
            .time +
        reggeWheelerSchwarzschildExteriorFactor
            frame.background *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .radial
            .radial +
        (1 / frame.background.radius ^ 2) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .theta
            .theta +
        (1 /
            (
              frame.background.radius *
                Real.sin frame.polarAngle
            ) ^ 2) *
          prizcarbonOddParityLinearizedRicciContraction
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            .phi
            .phi := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_linearizedRicciContribution
  ]

  exact
    prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution_eq_diagonal
      frame
      cpmJet
      harmonicJet

/--
The contraction is now reduced to four concrete diagonal components. No claim
that those components, or their weighted sum, vanish is made here.
-/
def prizcarbonOddParityVacuumCPMLinearizedRicciDiagonalBoundary : String :=
  "VACUUM_CPM_LINEARIZED_RICCI_DIAGONAL_EXPANSION_PROVED_FOUR_COMPONENT_CANCELLATION_OPEN"

end

end Chronos.Frontier
