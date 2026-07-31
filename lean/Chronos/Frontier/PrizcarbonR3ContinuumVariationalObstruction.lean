import Mathlib
import Chronos.Frontier.PrizcarbonR3CompactVariationalWitness
import Chronos.Frontier.PrizcarbonR3GalerkinInstability

namespace Chronos.Frontier

noncomputable section

/-!
# Prizcarbon r3 continuum variational obstruction

For the compact exterior coordinate `y = 2M/r`, the tortoise-coordinate
measure has density

`2M / (y²(1-y))`.

The explicit profile

`Ψ(y) = y⁴(1-y)`

has exact squared norm

`M/28`,

exact continuum quadratic energy

`(3r3+44)/(7920M)`,

and exact Rayleigh quotient

`7(3r3+44)/(1980M²)`.

For positive mass and `r3 < -44/3`, this gives an admissible positive-norm
continuum profile with strictly negative energy and strictly negative
Rayleigh quotient. Therefore the complete compact-coordinate continuum
quadratic form is not nonnegative.

This file does not claim that the full unbounded self-adjoint Schrödinger
operator, essential spectrum, negative discrete eigenvalue, or full PDE
growing mode have been formalized.
-/

/-- Compact-coordinate tortoise norm density. -/
def prizcarbonR3CompactContinuumNormDensity
    (mass : ℝ)
    (profile : ℝ → ℝ)
    (y : ℝ) : ℝ :=
  2 * mass * profile y ^ 2 /
    (y ^ 2 * (1 - y))

/-- Compact-coordinate static quadratic-energy density. -/
def prizcarbonR3CompactContinuumEnergyDensity
    (r3 : ℝ)
    (profile derivative : ℝ → ℝ)
    (y : ℝ) : ℝ :=
  prizcarbonR3CompactQuadraticDensity
    r3
    y
    (profile y)
    (derivative y)

/-- Compact-coordinate representation of the tortoise squared norm. -/
def prizcarbonR3CompactContinuumNormSquared
    (mass : ℝ)
    (profile : ℝ → ℝ) : ℝ :=
  ∫ y in (0 : ℝ)..1,
    prizcarbonR3CompactContinuumNormDensity
      mass
      profile
      y

/-- Dimensional compact-coordinate continuum quadratic energy. -/
def prizcarbonR3CompactContinuumQuadraticEnergy
    (r3 mass : ℝ)
    (profile derivative : ℝ → ℝ) : ℝ :=
  (
    ∫ y in (0 : ℝ)..1,
      prizcarbonR3CompactContinuumEnergyDensity
        r3
        profile
        derivative
        y
  ) /
    mass

/-- Continuum Rayleigh quotient. -/
def prizcarbonR3CompactContinuumRayleighQuotient
    (r3 mass : ℝ)
    (profile derivative : ℝ → ℝ) : ℝ :=
  prizcarbonR3CompactContinuumQuadraticEnergy
      r3
      mass
      profile
      derivative /
    prizcarbonR3CompactContinuumNormSquared
      mass
      profile

/-- Domain conditions for the compact-coordinate continuum form. -/
def PrizcarbonR3CompactContinuumAdmissible
    (r3 mass : ℝ)
    (profile derivative : ℝ → ℝ) : Prop :=
  (
    ∀ y : ℝ,
      HasDerivAt
        profile
        (derivative y)
        y
  ) ∧
    profile 0 = 0 ∧
    profile 1 = 0 ∧
    IntervalIntegrable
      (
        prizcarbonR3CompactContinuumNormDensity
          mass
          profile
      )
      MeasureTheory.volume
      0
      1 ∧
    IntervalIntegrable
      (
        prizcarbonR3CompactContinuumEnergyDensity
          r3
          profile
          derivative
      )
      MeasureTheory.volume
      0
      1

/-- Nonnegativity of the form on every admissible positive-norm profile. -/
def PrizcarbonR3CompactContinuumFormNonnegative
    (r3 mass : ℝ) : Prop :=
  ∀ (profile derivative : ℝ → ℝ),
    PrizcarbonR3CompactContinuumAdmissible
        r3
        mass
        profile
        derivative →
      0 <
          prizcarbonR3CompactContinuumNormSquared
            mass
            profile →
        0 ≤
          prizcarbonR3CompactContinuumQuadraticEnergy
            r3
            mass
            profile
            derivative

/--
The explicit profile's tortoise norm density equals the polynomial norm
density already integrated in the Galerkin theorem.
-/
theorem
    prizcarbonR3CompactContinuumTrialNormDensity_eq
    (mass y : ℝ) :
    prizcarbonR3CompactContinuumNormDensity
        mass
        prizcarbonR3CompactTrialProfile
        y =
      prizcarbonR3GalerkinNormDensity
        mass
        y := by
  by_cases hyZero : y = 0

  · subst y

    norm_num [
      prizcarbonR3CompactContinuumNormDensity,
      prizcarbonR3CompactTrialProfile,
      prizcarbonR3GalerkinNormDensity
    ]

  by_cases hyOne : y = 1

  · subst y

    norm_num [
      prizcarbonR3CompactContinuumNormDensity,
      prizcarbonR3CompactTrialProfile,
      prizcarbonR3GalerkinNormDensity
    ]

  have hySquareNonzero :
      y ^ 2 ≠ 0 :=
    pow_ne_zero
      2
      hyZero

  have hOneSubNonzero :
      1 - y ≠ 0 :=
    sub_ne_zero.mpr
      (
        Ne.symm
          hyOne
      )

  have hDenominatorNonzero :
      y ^ 2 * (1 - y) ≠ 0 :=
    mul_ne_zero
      hySquareNonzero
      hOneSubNonzero

  unfold
    prizcarbonR3CompactContinuumNormDensity
    prizcarbonR3CompactTrialProfile
    prizcarbonR3GalerkinNormDensity

  rw [
    div_eq_iff
      hDenominatorNonzero
  ]

  ring

/-- Function equality for the explicit norm densities. -/
theorem
    prizcarbonR3CompactContinuumTrialNormDensity_function_eq
    (mass : ℝ) :
    (
      prizcarbonR3CompactContinuumNormDensity
        mass
        prizcarbonR3CompactTrialProfile
    ) =
      prizcarbonR3GalerkinNormDensity mass := by
  funext y

  exact
    prizcarbonR3CompactContinuumTrialNormDensity_eq
      mass
      y

/-- The continuum trial energy density is the existing exact trial density. -/
theorem
    prizcarbonR3CompactContinuumTrialEnergyDensity_eq
    (r3 y : ℝ) :
    prizcarbonR3CompactContinuumEnergyDensity
        r3
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative
        y =
      prizcarbonR3CompactTrialDensity
        r3
        y := by
  rfl

/-- Function equality for the explicit energy densities. -/
theorem
    prizcarbonR3CompactContinuumTrialEnergyDensity_function_eq
    (r3 : ℝ) :
    (
      prizcarbonR3CompactContinuumEnergyDensity
        r3
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative
    ) =
      prizcarbonR3CompactTrialDensity r3 := by
  funext y

  exact
    prizcarbonR3CompactContinuumTrialEnergyDensity_eq
      r3
      y

/-- The explicit tortoise norm density is interval-integrable. -/
theorem
    prizcarbonR3CompactContinuumTrialNormDensity_intervalIntegrable
    (mass : ℝ) :
    IntervalIntegrable
      (
        prizcarbonR3CompactContinuumNormDensity
          mass
          prizcarbonR3CompactTrialProfile
      )
      MeasureTheory.volume
      0
      1 := by
  rw [
    prizcarbonR3CompactContinuumTrialNormDensity_function_eq
      mass
  ]

  exact
    (
      prizcarbonR3GalerkinNormDensity_continuous
        mass
    ).intervalIntegrable
      (μ := MeasureTheory.volume)
      0
      1

/-- The explicit continuum energy density is interval-integrable. -/
theorem
    prizcarbonR3CompactContinuumTrialEnergyDensity_intervalIntegrable
    (r3 : ℝ) :
    IntervalIntegrable
      (
        prizcarbonR3CompactContinuumEnergyDensity
          r3
          prizcarbonR3CompactTrialProfile
          prizcarbonR3CompactTrialProfileDerivative
      )
      MeasureTheory.volume
      0
      1 := by
  rw [
    prizcarbonR3CompactContinuumTrialEnergyDensity_function_eq
      r3
  ]

  exact
    (
      prizcarbonR3CompactTrialDensity_continuous
        r3
    ).intervalIntegrable
      (μ := MeasureTheory.volume)
      0
      1

/-- The explicit profile belongs to the continuum admissible domain. -/
theorem
    prizcarbonR3CompactContinuumTrial_admissible
    (r3 mass : ℝ) :
    PrizcarbonR3CompactContinuumAdmissible
      r3
      mass
      prizcarbonR3CompactTrialProfile
      prizcarbonR3CompactTrialProfileDerivative := by
  exact
    ⟨
      prizcarbonR3CompactTrialProfile_hasDerivAt,
      prizcarbonR3CompactTrialProfile_zero,
      prizcarbonR3CompactTrialProfile_one,
      prizcarbonR3CompactContinuumTrialNormDensity_intervalIntegrable
        mass,
      prizcarbonR3CompactContinuumTrialEnergyDensity_intervalIntegrable
        r3
    ⟩

/-- Exact continuum trial norm. -/
theorem
    prizcarbonR3CompactContinuumTrialNormSquared_exact
    (mass : ℝ) :
    prizcarbonR3CompactContinuumNormSquared
        mass
        prizcarbonR3CompactTrialProfile =
      mass / 28 := by
  unfold
    prizcarbonR3CompactContinuumNormSquared

  rw [
    prizcarbonR3CompactContinuumTrialNormDensity_function_eq
      mass
  ]

  exact
    prizcarbonR3GalerkinNormSquared_exact
      mass

/-- Positive continuum trial norm for positive mass. -/
theorem
    prizcarbonR3CompactContinuumTrialNormSquared_pos
    {mass : ℝ}
    (hMass : 0 < mass) :
    0 <
      prizcarbonR3CompactContinuumNormSquared
        mass
        prizcarbonR3CompactTrialProfile := by
  rw [
    prizcarbonR3CompactContinuumTrialNormSquared_exact
  ]

  exact
    div_pos
      hMass
      (by norm_num)

/-- The continuum trial energy is the existing exact compact energy. -/
theorem
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_eq_existing
    (r3 mass : ℝ) :
    prizcarbonR3CompactContinuumQuadraticEnergy
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative =
      prizcarbonR3CompactTrialQuadraticEnergy
        r3
        mass := by
  unfold
    prizcarbonR3CompactContinuumQuadraticEnergy
    prizcarbonR3CompactTrialQuadraticEnergy

  rw [
    prizcarbonR3CompactContinuumTrialEnergyDensity_function_eq
      r3
  ]

/-- Exact continuum trial quadratic energy. -/
theorem
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_exact
    (r3 mass : ℝ) :
    prizcarbonR3CompactContinuumQuadraticEnergy
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative =
      (3 * r3 + 44) /
        (7920 * mass) := by
  rw [
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_eq_existing
  ]

  exact
    prizcarbonR3CompactTrialQuadraticEnergy_exact
      r3
      mass

/-- Strictly negative continuum energy below the exact threshold. -/
theorem
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_neg
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    prizcarbonR3CompactContinuumQuadraticEnergy
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative <
      0 := by
  rw [
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_eq_existing
  ]

  exact
    prizcarbonR3CompactTrialQuadraticEnergy_neg
      hMass
      hR3

/-- Exact continuum Rayleigh quotient. -/
theorem
    prizcarbonR3CompactContinuumTrialRayleighQuotient_exact
    {r3 mass : ℝ}
    (hMass : mass ≠ 0) :
    prizcarbonR3CompactContinuumRayleighQuotient
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative =
      prizcarbonR3GalerkinEigenvalue
        r3
        mass := by
  unfold
    prizcarbonR3CompactContinuumRayleighQuotient

  rw [
    prizcarbonR3CompactContinuumTrialQuadraticEnergy_exact,
    prizcarbonR3CompactContinuumTrialNormSquared_exact
  ]

  unfold prizcarbonR3GalerkinEigenvalue

  field_simp [
    hMass
  ]

  ring

/-- Strictly negative continuum Rayleigh quotient below the threshold. -/
theorem
    prizcarbonR3CompactContinuumTrialRayleighQuotient_neg
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    prizcarbonR3CompactContinuumRayleighQuotient
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative <
      0 := by
  rw [
    prizcarbonR3CompactContinuumTrialRayleighQuotient_exact
      (
        ne_of_gt
          hMass
      )
  ]

  exact
    prizcarbonR3GalerkinEigenvalue_neg
      hMass
      hR3

/-- The complete continuum form cannot be nonnegative below the threshold. -/
theorem
    prizcarbonR3CompactContinuumForm_not_nonnegative
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    ¬
      PrizcarbonR3CompactContinuumFormNonnegative
        r3
        mass := by
  intro hNonnegative

  have hTrialNonnegative :
      0 ≤
        prizcarbonR3CompactContinuumQuadraticEnergy
          r3
          mass
          prizcarbonR3CompactTrialProfile
          prizcarbonR3CompactTrialProfileDerivative :=
    hNonnegative
      prizcarbonR3CompactTrialProfile
      prizcarbonR3CompactTrialProfileDerivative
      (
        prizcarbonR3CompactContinuumTrial_admissible
          r3
          mass
      )
      (
        prizcarbonR3CompactContinuumTrialNormSquared_pos
          hMass
      )

  exact
    (
      not_lt_of_ge
        hTrialNonnegative
    )
      (
        prizcarbonR3CompactContinuumTrialQuadraticEnergy_neg
          hMass
          hR3
      )

/-- Exact certificate for the continuum variational obstruction. -/
structure PrizcarbonR3ContinuumVariationalObstructionCertificate
    (r3 mass : ℝ) : Prop where
  trialAdmissible :
    PrizcarbonR3CompactContinuumAdmissible
      r3
      mass
      prizcarbonR3CompactTrialProfile
      prizcarbonR3CompactTrialProfileDerivative

  trialNormExact :
    prizcarbonR3CompactContinuumNormSquared
        mass
        prizcarbonR3CompactTrialProfile =
      mass / 28

  trialNormPositive :
    0 <
      prizcarbonR3CompactContinuumNormSquared
        mass
        prizcarbonR3CompactTrialProfile

  trialEnergyExact :
    prizcarbonR3CompactContinuumQuadraticEnergy
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative =
      (3 * r3 + 44) /
        (7920 * mass)

  trialEnergyNegative :
    prizcarbonR3CompactContinuumQuadraticEnergy
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative <
      0

  trialRayleighExact :
    prizcarbonR3CompactContinuumRayleighQuotient
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative =
      prizcarbonR3GalerkinEigenvalue
        r3
        mass

  trialRayleighNegative :
    prizcarbonR3CompactContinuumRayleighQuotient
        r3
        mass
        prizcarbonR3CompactTrialProfile
        prizcarbonR3CompactTrialProfileDerivative <
      0

  continuumFormNotNonnegative :
    ¬
      PrizcarbonR3CompactContinuumFormNonnegative
        r3
        mass

/--
For positive mass and `r3 < -44/3`, the explicit continuum profile is
admissible, has positive norm, negative energy, a negative Rayleigh quotient,
and disproves nonnegativity of the complete continuum form.
-/
theorem
    prizcarbonR3_exactContinuumVariationalObstruction
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    PrizcarbonR3ContinuumVariationalObstructionCertificate
      r3
      mass := by
  exact
    {
      trialAdmissible :=
        prizcarbonR3CompactContinuumTrial_admissible
          r3
          mass

      trialNormExact :=
        prizcarbonR3CompactContinuumTrialNormSquared_exact
          mass

      trialNormPositive :=
        prizcarbonR3CompactContinuumTrialNormSquared_pos
          hMass

      trialEnergyExact :=
        prizcarbonR3CompactContinuumTrialQuadraticEnergy_exact
          r3
          mass

      trialEnergyNegative :=
        prizcarbonR3CompactContinuumTrialQuadraticEnergy_neg
          hMass
          hR3

      trialRayleighExact :=
        prizcarbonR3CompactContinuumTrialRayleighQuotient_exact
          (
            ne_of_gt
              hMass
          )

      trialRayleighNegative :=
        prizcarbonR3CompactContinuumTrialRayleighQuotient_neg
          hMass
          hR3

      continuumFormNotNonnegative :=
        prizcarbonR3CompactContinuumForm_not_nonnegative
          hMass
          hR3
    }

def prizcarbonR3ContinuumVariationalObstructionStatus :
    String :=
  "EXACT_CONTINUUM_ADMISSIBLE_PROFILE_TORTOISE_NORM_QUADRATIC_ENERGY_NEGATIVE_RAYLEIGH_QUOTIENT_AND_FAILURE_OF_GLOBAL_FORM_NONNEGATIVITY_PROVED"

def prizcarbonR3ContinuumVariationalObstructionBoundary :
    String :=
  "FULL_UNBOUNDED_L2_REGGE_WHEELER_OPERATOR_SELF_ADJOINT_REALIZATION_ESSENTIAL_SPECTRUM_MIN_MAX_NEGATIVE_DISCRETE_EIGENVALUE_FULL_PDE_GROWING_MODE_AND_COVARIANT_PRIZCARBON_ORIGIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
