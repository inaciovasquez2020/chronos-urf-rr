import Chronos.Frontier.PrizcarbonOddParityLinearizedScalarCurvature
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMStaticTidalObservable

namespace Chronos.Frontier

noncomputable section

/--
The Prizcarbon scalar-curvature first variation specialized to the existing
vacuum CPM-derived metric and connection jets.
-/
def prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  prizcarbonOddParityLinearizedScalarCurvature
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

theorem
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_general
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
        frame
        cpmJet
        harmonicJet =
      prizcarbonOddParityLinearizedScalarCurvature
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
        ) := by
  rfl

def
    prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  prizcarbonOddParityInverseMetricBackgroundRicciContribution
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

def
    prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  prizcarbonOddParityBackgroundMetricLinearizedRicciContribution
    frame
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet
    )

theorem
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_contributions
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
        frame
        cpmJet
        harmonicJet =
      prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution
          frame
          cpmJet
          harmonicJet +
        prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution
          frame
          cpmJet
          harmonicJet := by
  rfl

def prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial
    (epsilon : ℝ)
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) : ℝ :=
  prizcarbonOddParityScalarCurvatureFirstOrderPolynomial
    epsilon
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

@[simp]
theorem
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial
        0
        frame
        cpmJet
        harmonicJet =
      0 := by
  simp [
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial
  ]

@[simp]
theorem
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial_one
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial
        1
        frame
        cpmJet
        harmonicJet =
      prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
        frame
        cpmJet
        harmonicJet := by
  unfold
    prizcarbonOddParityVacuumCPMScalarCurvatureFirstOrderPolynomial
  unfold
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
  exact
    prizcarbonOddParityScalarCurvatureFirstOrderPolynomial_one
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

/--
The concrete CPM specialization is complete, but no cancellation theorem is
claimed. Proving zero requires explicit component identities for the
specialized Ricci contractions.
-/
def prizcarbonOddParityVacuumCPMLinearizedScalarCurvatureBoundary : String :=
  "VACUUM_CPM_LINEARIZED_SCALAR_CURVATURE_SPECIALIZATION_COMPLETE_ZERO_NOT_YET_PROVED_REMAINING_ACTION_SCALAR_VARIATIONS_AND_ACTION_HESSIAN_OPEN"

end

end Chronos.Frontier
