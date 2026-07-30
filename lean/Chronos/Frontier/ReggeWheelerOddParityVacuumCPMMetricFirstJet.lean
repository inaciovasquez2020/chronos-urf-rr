import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMReconstruction
import Chronos.Frontier.ReggeWheelerOddParityLinearizedConnection

namespace Chronos.Frontier

noncomputable section

/--
A pointwise second jet of the vacuum Cunningham–Price–Moncrief master
amplitude.

The embedded first jet contains:

* `Ψ_CPM`;
* `∂ₜ Ψ_CPM`;
* `∂ᵣ Ψ_CPM`.

The additional fields provide the second derivatives needed to derive the
time and radial coordinate derivatives of the reconstructed odd-parity
metric coefficients.
-/
structure ReggeWheelerOddParityVacuumCPMSecondJet where
  firstJet : ReggeWheelerOddParityVacuumCPMFirstJet
  cpmTimeTimeDerivative : ℝ
  cpmTimeRadialDerivative : ℝ
  cpmRadialRadialDerivative : ℝ

/--
Coordinate first derivatives of the odd vector harmonic.

The harmonic values are supplied by the existing angular-harmonic carrier.
This structure adds only the four angular coordinate derivatives.
-/
structure ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet where
  harmonic : ReggeWheelerOddParityAngularHarmonicValue
  vectorCoordinatePartial :
    ReggeWheelerAngularCoordinate →
      ReggeWheelerAngularCoordinate →
        ℝ

/--
The exact radial derivative of the Schwarzschild exterior factor

`f(r) = 1 - 2M/r`:

`f'(r) = 2M/r²`.
-/
def reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) : ℝ :=
  2 * jet.firstJet.background.mass /
    jet.firstJet.background.radius ^ 2

/--
The CPM-derived time derivative of the time-angular metric coefficient:

`∂ₜh_t
  = f/2 * (∂ₜΨ_CPM + r ∂ₜ∂ᵣΨ_CPM)`.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) : ℝ :=
  reggeWheelerSchwarzschildExteriorFactor
        jet.firstJet.background /
      2 *
    (
      jet.firstJet.cpmTimeDerivative +
        jet.firstJet.background.radius *
          jet.cpmTimeRadialDerivative
    )

/--
The CPM-derived radial derivative of the time-angular metric coefficient:

`∂ᵣh_t
  = f'/2 * (Ψ_CPM + r ∂ᵣΨ_CPM)
    + f/2 * (2 ∂ᵣΨ_CPM + r ∂ᵣ²Ψ_CPM)`.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficientRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative jet /
        2 *
      (
        jet.firstJet.cpmAmplitude +
          jet.firstJet.background.radius *
            jet.firstJet.cpmRadialDerivative
      ) +
    reggeWheelerSchwarzschildExteriorFactor
          jet.firstJet.background /
        2 *
      (
        2 * jet.firstJet.cpmRadialDerivative +
          jet.firstJet.background.radius *
            jet.cpmRadialRadialDerivative
      )

/--
The CPM-derived time derivative of the radial-angular metric coefficient:

`∂ₜh_r = r/(2f) * ∂ₜ²Ψ_CPM`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientTimeDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) : ℝ :=
  reggeWheelerOddParityRWRadialCoefficientFromMaster
    jet.firstJet.background
    (jet.cpmTimeTimeDerivative / 2)

/--
The CPM-derived radial derivative of the radial-angular metric coefficient:

`∂ᵣh_r
  = (1/f - r f'/f²) * (∂ₜΨ_CPM/2)
    + (r/f) * (∂ₜ∂ᵣΨ_CPM/2)`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) : ℝ :=
  let factor :=
    reggeWheelerSchwarzschildExteriorFactor
      jet.firstJet.background

  let factorRadialDerivative :=
    reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative jet

  (
    1 / factor -
      jet.firstJet.background.radius *
        factorRadialDerivative /
        factor ^ 2
  ) *
      (jet.firstJet.cpmTimeDerivative / 2) +
    jet.firstJet.background.radius /
        factor *
      (jet.cpmTimeRadialDerivative / 2)

/--
Select the reconstructed odd-parity coefficient associated with a
non-angular coordinate index.
-/
def reggeWheelerOddParityVacuumCPMMetricCoefficient
    (jet : ReggeWheelerOddParityVacuumCPMFirstJet) :
    ReggeWheelerSpacetimeCoordinate → ℝ
  | .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficient jet
  | .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficient jet
  | .theta =>
      0
  | .phi =>
      0

/--
The time or radial derivative of a reconstructed odd-parity metric
coefficient.

The first coordinate is the derivative coordinate. The second coordinate
selects the time-angular or radial-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ℝ
  | .time, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative jet
  | .radial, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientRadialDerivative jet
  | .time, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientTimeDerivative jet
  | .radial, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative jet
  | _, _ =>
      0

/--
The derivative of one coefficient-times-vector-harmonic metric component.

For time and radial differentiation, the CPM-derived coefficient derivative
is used. For angular differentiation, the reconstructed coefficient is
multiplied by the supplied coordinate derivative of the vector harmonic.
-/
def reggeWheelerOddParityVacuumCPMMetricPartialEntry
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet)
    (derivative coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) : ℝ :=
  match derivative with
  | .time =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet .time coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.harmonic angularCoordinate
  | .radial =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet .radial coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.harmonic angularCoordinate
  | .theta =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinatePartial
          .theta angularCoordinate
  | .phi =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinatePartial
          .phi angularCoordinate

/--
The complete coordinate first derivative `∂_κ h_{μν}` of the
CPM-reconstructed odd-parity metric.

The only nonzero metric components are the symmetric time-angular and
radial-angular pairs. Their time and radial derivatives are fixed by the CPM
second jet. Their angular derivatives are fixed by the reconstructed
coefficient and the vector-harmonic coordinate first jet.
-/
def reggeWheelerOddParityVacuumCPMMetricPartial
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  | derivative, .time, .theta =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .time .theta
  | derivative, .theta, .time =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .time .theta

  | derivative, .time, .phi =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .time .phi
  | derivative, .phi, .time =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .time .phi

  | derivative, .radial, .theta =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .radial .theta
  | derivative, .theta, .radial =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .radial .theta

  | derivative, .radial, .phi =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .radial .phi
  | derivative, .phi, .radial =>
      reggeWheelerOddParityVacuumCPMMetricPartialEntry
        jet harmonicJet derivative .radial .phi

  | _, _, _ =>
      0

/--
The CPM and harmonic jets construct a concrete perturbation metric first jet
without accepting an arbitrary spacetime `metricPartial` function.
-/
def reggeWheelerOddParityVacuumCPMMetricFirstJet
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet) :
    ReggeWheelerOddParityMetricPerturbationFirstJet where
  metricValue :=
    reggeWheelerOddParitySpacetimeMetricPerturbation
      (reggeWheelerOddParityVacuumCPMMetricComponents jet.firstJet)
      harmonicJet.harmonic

  metricPartial :=
    reggeWheelerOddParityVacuumCPMMetricPartial
      jet harmonicJet

  metricValue_symmetric :=
    reggeWheelerOddParitySpacetimeMetricPerturbation_symmetric
      (reggeWheelerOddParityVacuumCPMMetricComponents jet.firstJet)
      harmonicJet.harmonic

  metricPartial_symmetric := by
    intro derivative left right
    cases derivative <;>
      cases left <;>
        cases right <;>
          rfl

/--
The constructed first jet contains the assembled CPM-reconstructed metric
exactly.
-/
theorem reggeWheelerOddParityVacuumCPMMetricFirstJet_metricValue
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricValue =
      reggeWheelerOddParitySpacetimeMetricPerturbation
        (reggeWheelerOddParityVacuumCPMMetricComponents jet.firstJet)
        harmonicJet.harmonic := by
  rfl

/--
Representative identities proving that all four time/radial derivatives of
the two nonzero odd-parity metric coefficients are fixed by the CPM second
jet.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricFirstJet_reconstructsTimeRadialDerivatives
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricPartial .time .time .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.harmonic .theta ∧
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricPartial .radial .time .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientRadialDerivative jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.harmonic .theta ∧
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricPartial .time .radial .theta =
        reggeWheelerOddParityVacuumCPMRadialCoefficientTimeDerivative jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.harmonic .theta ∧
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricPartial .radial .radial .theta =
        reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.harmonic .theta := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/--
A representative angular derivative is fixed by the reconstructed metric
coefficient and the corresponding vector-harmonic coordinate derivative.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricFirstJet_angularDerivative
    (jet : ReggeWheelerOddParityVacuumCPMSecondJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet harmonicJet
    ).metricPartial .theta .time .phi =
      reggeWheelerOddParityVacuumCPMTimeCoefficient jet.firstJet *
        harmonicJet.vectorCoordinatePartial .theta .phi := by
  rfl

def reggeWheelerOddParityVacuumCPMMetricFirstJetBoundary : String :=
  "VACUUM_CPM_SECOND_JET_DERIVES_TIME_AND_RADIAL_FIRST_DERIVATIVES_OF_BOTH_ODD_METRIC_COEFFICIENTS_AND_CONSTRUCTS_THE_METRIC_FIRST_JET_WITHOUT_AN_ARBITRARY_SPACETIME_METRIC_PARTIAL_FUNCTION_ANGULAR_HARMONIC_COORDINATE_DERIVATIVES_REMAIN_SUPPLIED_CPM_SECOND_JET_NOT_WAVE_EVOLUTION_DERIVED_CONNECTION_PARTIALS_FREE_FALL_RESPONSE_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
