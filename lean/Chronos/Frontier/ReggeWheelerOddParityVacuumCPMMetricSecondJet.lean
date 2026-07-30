import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityDerivedLinearizedConnectionFirstJet

namespace Chronos.Frontier

noncomputable section

/--
A pointwise third jet of the vacuum Cunningham–Price–Moncrief master
amplitude.

The embedded second jet contains the amplitude, first derivatives, and second
derivatives. The additional fields provide the third derivatives needed to
derive the complete metric second jet.
-/
structure ReggeWheelerOddParityVacuumCPMThirdJet where
  secondJet : ReggeWheelerOddParityVacuumCPMSecondJet
  cpmTimeTimeTimeDerivative : ℝ
  cpmTimeTimeRadialDerivative : ℝ
  cpmTimeRadialRadialDerivative : ℝ
  cpmRadialRadialRadialDerivative : ℝ

/--
A coordinate second jet of the odd vector harmonic.

The embedded first jet contains the harmonic and its first angular coordinate
derivatives. The additional field supplies its second angular coordinate
derivatives.
-/
structure ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet where
  firstJet : ReggeWheelerOddParityVectorHarmonicCoordinateFirstJet
  vectorCoordinateSecondPartial :
    ReggeWheelerAngularCoordinate →
      ReggeWheelerAngularCoordinate →
        ReggeWheelerAngularCoordinate →
          ℝ

/--
The second radial derivative of the Schwarzschild exterior factor:

`f''(r) = -4M/r³`.
-/
def reggeWheelerOddParityVacuumCPMExteriorFactorSecondRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  -4 * jet.secondJet.firstJet.background.mass /
    jet.secondJet.firstJet.background.radius ^ 3

/--
The second time derivative of the reconstructed time-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficientTimeTimeDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerSchwarzschildExteriorFactor
        jet.secondJet.firstJet.background /
      2 *
    (
      jet.secondJet.cpmTimeTimeDerivative +
        jet.secondJet.firstJet.background.radius *
          jet.cpmTimeTimeRadialDerivative
    )

/--
The mixed time-radial derivative of the reconstructed time-angular
coefficient.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
        jet.secondJet /
      2 *
      (
        jet.secondJet.firstJet.cpmTimeDerivative +
          jet.secondJet.firstJet.background.radius *
            jet.secondJet.cpmTimeRadialDerivative
      ) +
    reggeWheelerSchwarzschildExteriorFactor
          jet.secondJet.firstJet.background /
        2 *
      (
        2 * jet.secondJet.cpmTimeRadialDerivative +
          jet.secondJet.firstJet.background.radius *
            jet.cpmTimeRadialRadialDerivative
      )

/--
The second radial derivative of the reconstructed time-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMTimeCoefficientRadialRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMExteriorFactorSecondRadialDerivative
        jet /
      2 *
      (
        jet.secondJet.firstJet.cpmAmplitude +
          jet.secondJet.firstJet.background.radius *
            jet.secondJet.firstJet.cpmRadialDerivative
      ) +
    reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
        jet.secondJet *
      (
        2 * jet.secondJet.firstJet.cpmRadialDerivative +
          jet.secondJet.firstJet.background.radius *
            jet.secondJet.cpmRadialRadialDerivative
      ) +
    reggeWheelerSchwarzschildExteriorFactor
          jet.secondJet.firstJet.background /
        2 *
      (
        3 * jet.secondJet.cpmRadialRadialDerivative +
          jet.secondJet.firstJet.background.radius *
            jet.cpmRadialRadialRadialDerivative
      )

/--
The radial coefficient multiplier

`q(r) = r/(2f(r))`

in `h_r = q(r) ∂ₜΨ_CPM`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplier
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  jet.secondJet.firstJet.background.radius /
    (
      2 *
        reggeWheelerSchwarzschildExteriorFactor
          jet.secondJet.firstJet.background
    )

/--
The first radial derivative of `q(r) = r/(2f(r))`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplierFirstDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  1 /
        (
          2 *
            reggeWheelerSchwarzschildExteriorFactor
              jet.secondJet.firstJet.background
        ) -
    jet.secondJet.firstJet.background.radius *
        reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
          jet.secondJet /
      (
        2 *
          (
            reggeWheelerSchwarzschildExteriorFactor
              jet.secondJet.firstJet.background
          ) ^ 2
      )

/--
The second radial derivative of `q(r) = r/(2f(r))`.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplierSecondDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  -reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
          jet.secondJet /
      (
        reggeWheelerSchwarzschildExteriorFactor
          jet.secondJet.firstJet.background
      ) ^ 2 -
    jet.secondJet.firstJet.background.radius *
        reggeWheelerOddParityVacuumCPMExteriorFactorSecondRadialDerivative
          jet /
      (
        2 *
          (
            reggeWheelerSchwarzschildExteriorFactor
              jet.secondJet.firstJet.background
          ) ^ 2
      ) +
    jet.secondJet.firstJet.background.radius *
        (
          reggeWheelerOddParityVacuumCPMExteriorFactorRadialDerivative
            jet.secondJet
        ) ^ 2 /
      (
        reggeWheelerSchwarzschildExteriorFactor
          jet.secondJet.firstJet.background
      ) ^ 3

/--
The second time derivative of the reconstructed radial-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplier jet *
    jet.cpmTimeTimeTimeDerivative

/--
The mixed time-radial derivative of the reconstructed radial-angular
coefficient.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientTimeRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplierFirstDerivative
        jet *
      jet.secondJet.cpmTimeTimeDerivative +
    reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplier jet *
      jet.cpmTimeTimeRadialDerivative

/--
The second radial derivative of the reconstructed radial-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMRadialCoefficientRadialRadialDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) : ℝ :=
  reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplierSecondDerivative
        jet *
      jet.secondJet.firstJet.cpmTimeDerivative +
    2 *
        reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplierFirstDerivative
          jet *
      jet.secondJet.cpmTimeRadialDerivative +
    reggeWheelerOddParityVacuumCPMRadialCoefficientMultiplier jet *
      jet.cpmTimeRadialRadialDerivative

/--
Select a second time/radial derivative of one reconstructed odd-parity metric
coefficient.

The first two coordinates are derivative indices. The third selects the
time-angular or radial-angular coefficient.
-/
def reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ℝ
  | .time, .time, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientTimeTimeDerivative jet

  | .time, .radial, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative jet

  | .radial, .time, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative jet

  | .radial, .radial, .time =>
      reggeWheelerOddParityVacuumCPMTimeCoefficientRadialRadialDerivative
        jet

  | .time, .time, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative jet

  | .time, .radial, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientTimeRadialDerivative
        jet

  | .radial, .time, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientTimeRadialDerivative
        jet

  | .radial, .radial, .radial =>
      reggeWheelerOddParityVacuumCPMRadialCoefficientRadialRadialDerivative
        jet

  | _, _, _ =>
      0

/--
One second derivative of a coefficient-times-vector-harmonic metric
component.

This covers two time/radial derivatives, mixed coefficient-angular
derivatives, and purely angular derivatives.
-/
def reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) : ℝ :=
  match derivativeOuter, derivativeInner with
  | .time, .time =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
          jet .time .time coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic angularCoordinate

  | .time, .radial =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
          jet .time .radial coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic angularCoordinate

  | .radial, .time =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
          jet .radial .time coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic angularCoordinate

  | .radial, .radial =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
          jet .radial .radial coefficientCoordinate *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic angularCoordinate

  | .time, .theta =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .time coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .theta angularCoordinate

  | .theta, .time =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .time coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .theta angularCoordinate

  | .time, .phi =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .time coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .phi angularCoordinate

  | .phi, .time =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .time coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .phi angularCoordinate

  | .radial, .theta =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .radial coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .theta angularCoordinate

  | .theta, .radial =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .radial coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .theta angularCoordinate

  | .radial, .phi =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .radial coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .phi angularCoordinate

  | .phi, .radial =>
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .radial coefficientCoordinate *
        harmonicJet.firstJet.vectorCoordinatePartial
          .phi angularCoordinate

  | .theta, .theta =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.secondJet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinateSecondPartial
          .theta .theta angularCoordinate

  | .theta, .phi =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.secondJet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinateSecondPartial
          .theta .phi angularCoordinate

  | .phi, .theta =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.secondJet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinateSecondPartial
          .phi .theta angularCoordinate

  | .phi, .phi =>
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.secondJet.firstJet coefficientCoordinate *
        harmonicJet.vectorCoordinateSecondPartial
          .phi .phi angularCoordinate

/--
The complete second coordinate partial `∂_κ∂_λh_{μν}` of the
CPM-reconstructed odd-parity metric.
-/
def reggeWheelerOddParityVacuumCPMMetricSecondPartial
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ
  | derivativeOuter, derivativeInner, .time, .theta =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .time .theta

  | derivativeOuter, derivativeInner, .theta, .time =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .time .theta

  | derivativeOuter, derivativeInner, .time, .phi =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .time .phi

  | derivativeOuter, derivativeInner, .phi, .time =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .time .phi

  | derivativeOuter, derivativeInner, .radial, .theta =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .radial .theta

  | derivativeOuter, derivativeInner, .theta, .radial =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .radial .theta

  | derivativeOuter, derivativeInner, .radial, .phi =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .radial .phi

  | derivativeOuter, derivativeInner, .phi, .radial =>
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        jet harmonicJet derivativeOuter derivativeInner .radial .phi

  | _, _, _, _ =>
      0

/--
Construct the metric second jet directly from one CPM third jet and one
vector-harmonic coordinate second jet.

No arbitrary spacetime `metricSecondPartial` function is accepted.
-/
def reggeWheelerOddParityVacuumCPMMetricSecondJet
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    ReggeWheelerOddParityMetricPerturbationSecondJet where
  firstJet :=
    reggeWheelerOddParityVacuumCPMMetricFirstJet
      jet.secondJet
      harmonicJet.firstJet

  metricSecondPartial :=
    reggeWheelerOddParityVacuumCPMMetricSecondPartial
      jet
      harmonicJet

/--
The constructed metric second jet contains the previously established
CPM-derived metric first jet exactly.
-/
theorem reggeWheelerOddParityVacuumCPMMetricSecondJet_firstJet
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).firstJet =
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        jet.secondJet
        harmonicJet.firstJet := by
  rfl

/--
Representative identities proving that all six time/radial second
derivatives of the two nonzero metric coefficients are fixed by one CPM
third jet.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondJet_reconstructsTimeRadialSecondDerivatives
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .time .time .time .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeTimeDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta ∧

    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .time .radial .time .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta ∧

    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .radial .radial .time .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientRadialRadialDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta ∧

    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .time .time .radial .theta =
        reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta ∧

    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .time .radial .radial .theta =
        reggeWheelerOddParityVacuumCPMRadialCoefficientTimeRadialDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta ∧

    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .radial .radial .radial .theta =
        reggeWheelerOddParityVacuumCPMRadialCoefficientRadialRadialDerivative
            jet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic .theta := by
  exact ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

/--
A mixed radial-angular second derivative is reconstructed from the CPM
coefficient first derivative and the vector-harmonic first derivative.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondJet_mixedAngularDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .radial .theta .time .phi =
      reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
          jet.secondJet .radial .time *
        harmonicJet.firstJet.vectorCoordinatePartial
          .theta .phi := by
  rfl

/--
A purely angular second derivative is reconstructed from the metric
coefficient and the vector-harmonic second derivative.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondJet_angularAngularDerivative
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        jet harmonicJet
    ).metricSecondPartial .theta .phi .radial .theta =
      reggeWheelerOddParityVacuumCPMMetricCoefficient
          jet.secondJet.firstJet .radial *
        harmonicJet.vectorCoordinateSecondPartial
          .theta .phi .theta := by
  rfl

def reggeWheelerOddParityVacuumCPMMetricSecondJetBoundary : String :=
  "VACUUM_CPM_THIRD_JET_AND_VECTOR_HARMONIC_SECOND_JET_CONSTRUCT_THE_COMPLETE_ODD_METRIC_SECOND_PARTIAL_WITHOUT_AN_ARBITRARY_SPACETIME_METRIC_SECOND_PARTIAL_FUNCTION_CPM_THIRD_JET_AND_ANGULAR_HARMONIC_SECOND_DERIVATIVES_REMAIN_LOCAL_SUPPLIED_DATA_RATHER_THAN_WAVE_AND_HARMONIC_EQUATION_DERIVED_FREE_FALL_RESPONSE_AND_PHYSICAL_STRAIN_NOT_PROVED"

end

end Chronos.Frontier
