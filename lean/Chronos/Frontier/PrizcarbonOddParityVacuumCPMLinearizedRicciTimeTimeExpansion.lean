import Chronos.Frontier.PrizcarbonOddParityVacuumCPMLinearizedRicciDiagonalExpansion

namespace Chronos.Frontier

noncomputable section

/--
The concrete vacuum-CPM time-time component of the linearized Ricci tensor.

This is the Ricci contraction of the concrete CPM-derived linearized
connection jet with both free indices fixed to the Schwarzschild time
coordinate.
-/
def prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  prizcarbonOddParityLinearizedRicciContraction
    frame
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet
    )
    .time
    .time

/--
The vacuum-CPM time-time linearized Ricci component is exactly the explicit
four-coordinate contraction

`δR_tt = Σ_α δR^α_{ t α t }`.

No individual linearized-Riemann component is declared to vanish.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_contractedRiemannCoordinates
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
          .time
          .time
          .time
          .time +
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
  rfl

/--
The time-weighted term appearing in the diagonal scalar-curvature expansion.
-/
def prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  -(1 /
      reggeWheelerSchwarzschildExteriorFactor
        frame.background) *
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime
      frame
      cpmJet
      harmonicJet

/--
The time-weighted scalar-curvature contribution inherits the same explicit
four-coordinate linearized-Riemann expansion.
-/
theorem
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution_eq_contractedRiemannCoordinates
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
              .time
              .time
              .time
              .time +
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
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_contractedRiemannCoordinates
  ]

/--
The time-time Ricci component is now expanded into concrete linearized-Riemann
coordinates. No zero theorem or cancellation theorem has yet been established.
-/
def prizcarbonOddParityVacuumCPMLinearizedRicciTimeTimeBoundary : String :=
  "VACUUM_CPM_TIME_TIME_LINEARIZED_RICCI_EXPANDED_COMPONENT_ZERO_AND_CANCELLATION_OPEN"

end

end Chronos.Frontier
