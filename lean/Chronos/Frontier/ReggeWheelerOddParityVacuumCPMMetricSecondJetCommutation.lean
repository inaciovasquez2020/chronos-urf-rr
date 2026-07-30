import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricSecondJet

namespace Chronos.Frontier

noncomputable section

/--
The reconstructed coefficient second partials commute in their two
time/radial derivative indices.

The coefficient coordinate must be split because the existing definition
pattern-matches jointly on all three coordinates.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial_derivatives_commute
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
        cpmJet
        derivativeOuter
        derivativeInner
        coefficientCoordinate =
      reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
        cpmJet
        derivativeInner
        derivativeOuter
        coefficientCoordinate := by
  cases derivativeOuter <;>
    cases derivativeInner <;>
      cases coefficientCoordinate <;>
        rfl

/--
One coefficient-times-vector-harmonic metric entry has commuting second
coordinate derivatives, conditional on commutation of the supplied angular
harmonic second partials.

The hypothesis is explicit because the current repository stores the angular
second derivatives as raw local data and does not derive their mixed-partial
symmetry from concrete spherical-harmonic formulas.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry_derivatives_commute
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        cpmJet
        harmonicJet
        derivativeOuter
        derivativeInner
        coefficientCoordinate
        angularCoordinate =
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        cpmJet
        harmonicJet
        derivativeInner
        derivativeOuter
        coefficientCoordinate
        angularCoordinate := by
  cases derivativeOuter <;>
    cases derivativeInner <;>
      cases coefficientCoordinate <;>
        cases angularCoordinate <;>
          simp [
            reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry,
            reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial,
            hHarmonicSymm
          ]

/--
The complete CPM-reconstructed odd-parity metric second partial commutes in
its two derivative coordinates, conditional on the supplied angular
mixed-partial symmetry:

`∂_κ ∂_λ h_{μν} = ∂_λ ∂_κ h_{μν}`.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondPartial_derivatives_commute
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartial
        cpmJet
        harmonicJet
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight =
      reggeWheelerOddParityVacuumCPMMetricSecondPartial
        cpmJet
        harmonicJet
        derivativeInner
        derivativeOuter
        metricLeft
        metricRight := by
  cases derivativeOuter <;>
    cases derivativeInner <;>
      cases metricLeft <;>
        cases metricRight <;>
          simp [
            reggeWheelerOddParityVacuumCPMMetricSecondPartial,
            reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry,
            reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial,
            hHarmonicSymm
          ]

/--
The existing concrete CPM metric second jet inherits derivative commutation
from the explicit angular harmonic mixed-partial symmetry hypothesis.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondJet_derivatives_commute
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight =
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet
          cpmJet
          harmonicJet
      ).metricSecondPartial
        derivativeInner
        derivativeOuter
        metricLeft
        metricRight := by
  exact
    reggeWheelerOddParityVacuumCPMMetricSecondPartial_derivatives_commute
      cpmJet
      harmonicJet
      hHarmonicSymm
      derivativeOuter
      derivativeInner
      metricLeft
      metricRight

def reggeWheelerOddParityVacuumCPMMetricSecondJetCommutationBoundary :
    String :=
  "CPM_METRIC_SECOND_DERIVATIVE_COMMUTATION_IS_PROVED_CONDITIONALLY_FROM_ONE_EXPLICIT_ANGULAR_HARMONIC_SECOND_PARTIAL_SYMMETRY_HYPOTHESIS_NO_COMPATIBLE_WRAPPER_TYPE_OR_UNCONDITIONAL_CLAIRAUT_CLAIM_IS_INTRODUCED_THE_HARMONIC_SYMMETRY_HYPOTHESIS_REMAINS_UNDISCHARGED_UNTIL_EXPLICIT_SPHERICAL_HARMONIC_FORMULAS_OR_A_REGULARITY_THEOREM_ARE_PROVIDED_LOWERED_RIEMANN_PAIR_EXCHANGE_TIDAL_MATRIX_SYMMETRY_GLOBAL_GEODESIC_EVOLUTION_FRAME_TRANSPORT_AND_INTEGRATED_PHYSICAL_STRAIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
