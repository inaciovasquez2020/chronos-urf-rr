import Mathlib
import Chronos.Frontier.ReggeWheelerBoundedPotentialResponse
import Chronos.Frontier.ReggeWheelerOddParityMasterExtraction

namespace Chronos.Frontier

noncomputable section

/-!
# Prizcarbon r3 compact variational witness

For the quadrupole test potential

`V_r3(r) = f(r) [6/r² + (r3 - 6) M/r³]`

and compact exterior coordinate `y = 2M/r`, the reduced static quadratic
density is modeled by

`1/2 (1-y)y² (∂y Ψ)² + [3 + (r3-6)y/4] Ψ²`.

The explicit profile

`Ψ(y) = y⁴(1-y)`

has exact reduced quadratic energy

`(3r3 + 44)/(7920M)`.

Consequently, positive mass and `r3 < -44/3` give a strictly negative
quadratic witness.

This file does not claim a self-adjoint operator, negative eigenvalue,
exponentially growing mode, or covariant origin for the r3 term.
-/

/-- Potential coefficient in the reduced compact-coordinate density. -/
def prizcarbonR3CompactPotentialCoefficient
    (r3 y : ℝ) : ℝ :=
  3 + (r3 - 6) * y / 4

/-- Reduced compact-coordinate quadratic density. -/
def prizcarbonR3CompactQuadraticDensity
    (r3 y profileValue profileDerivative : ℝ) : ℝ :=
  (1 / 2 : ℝ) *
      (1 - y) *
      y ^ 2 *
      profileDerivative ^ 2 +
    prizcarbonR3CompactPotentialCoefficient r3 y *
      profileValue ^ 2

/-- Polynomial profile vanishing at both compact-coordinate endpoints. -/
def prizcarbonR3CompactTrialProfile
    (y : ℝ) : ℝ :=
  y ^ 4 * (1 - y)

/-- Exact derivative of the polynomial trial profile. -/
def prizcarbonR3CompactTrialProfileDerivative
    (y : ℝ) : ℝ :=
  4 * y ^ 3 - 5 * y ^ 4

theorem prizcarbonR3CompactTrialProfile_hasDerivAt
    (y : ℝ) :
    HasDerivAt
        prizcarbonR3CompactTrialProfile
        (prizcarbonR3CompactTrialProfileDerivative y)
        y := by
  unfold
    prizcarbonR3CompactTrialProfile
    prizcarbonR3CompactTrialProfileDerivative

  convert
    ((hasDerivAt_id y).pow 4).mul
      (
        (hasDerivAt_const y (1 : ℝ)).sub
          (hasDerivAt_id y)
      )
    using 1

  simp [id]
  ring

theorem prizcarbonR3CompactTrialProfile_zero :
    prizcarbonR3CompactTrialProfile 0 =
      0 := by
  norm_num [
    prizcarbonR3CompactTrialProfile
  ]

theorem prizcarbonR3CompactTrialProfile_one :
    prizcarbonR3CompactTrialProfile 1 =
      0 := by
  norm_num [
    prizcarbonR3CompactTrialProfile
  ]

/-- Quadratic density evaluated on the explicit profile. -/
def prizcarbonR3CompactTrialDensity
    (r3 y : ℝ) : ℝ :=
  prizcarbonR3CompactQuadraticDensity
    r3
    y
    (prizcarbonR3CompactTrialProfile y)
    (prizcarbonR3CompactTrialProfileDerivative y)

/-- Expanded polynomial form of the trial density. -/
theorem prizcarbonR3CompactTrialDensity_expanded
    (r3 y : ℝ) :
    prizcarbonR3CompactTrialDensity r3 y =
      r3 * y ^ 11 / 4 -
        r3 * y ^ 10 / 2 +
        r3 * y ^ 9 / 4 -
        14 * y ^ 11 +
        77 * y ^ 10 / 2 -
        71 * y ^ 9 / 2 +
        11 * y ^ 8 := by
  unfold
    prizcarbonR3CompactTrialDensity
    prizcarbonR3CompactQuadraticDensity
    prizcarbonR3CompactPotentialCoefficient
    prizcarbonR3CompactTrialProfile
    prizcarbonR3CompactTrialProfileDerivative

  ring

/-- Exact polynomial primitive of the trial density. -/
def prizcarbonR3CompactTrialPrimitive
    (r3 y : ℝ) : ℝ :=
  (r3 / 48) * y ^ 12 -
    (r3 / 22) * y ^ 11 +
    (r3 / 40) * y ^ 10 -
    (7 / 6 : ℝ) * y ^ 12 +
    (7 / 2 : ℝ) * y ^ 11 -
    (71 / 20 : ℝ) * y ^ 10 +
    (11 / 9 : ℝ) * y ^ 9

private theorem hasDerivAt_const_mul_pow
    (coefficient : ℝ)
    (power : ℕ)
    (y : ℝ) :
    HasDerivAt
        (fun z : ℝ =>
          coefficient * z ^ power)
        (
          coefficient *
            ((power : ℝ) *
              y ^ (power - 1))
        )
        y := by
  simpa [id, mul_assoc] using
    ((hasDerivAt_id y).pow power).const_mul
      coefficient

theorem prizcarbonR3CompactTrialPrimitive_hasDerivAt
    (r3 y : ℝ) :
    HasDerivAt
        (prizcarbonR3CompactTrialPrimitive r3)
        (prizcarbonR3CompactTrialDensity r3 y)
        y := by
  have hR12 :
      HasDerivAt
          (fun z : ℝ =>
            (r3 / 48) * z ^ 12)
          (
            (r3 / 48) *
              ((12 : ℝ) * y ^ 11)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (r3 / 48)
        12
        y

  have hR11 :
      HasDerivAt
          (fun z : ℝ =>
            (r3 / 22) * z ^ 11)
          (
            (r3 / 22) *
              ((11 : ℝ) * y ^ 10)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (r3 / 22)
        11
        y

  have hR10 :
      HasDerivAt
          (fun z : ℝ =>
            (r3 / 40) * z ^ 10)
          (
            (r3 / 40) *
              ((10 : ℝ) * y ^ 9)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (r3 / 40)
        10
        y

  have h12 :
      HasDerivAt
          (fun z : ℝ =>
            (7 / 6 : ℝ) * z ^ 12)
          (
            (7 / 6 : ℝ) *
              ((12 : ℝ) * y ^ 11)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (7 / 6 : ℝ)
        12
        y

  have h11 :
      HasDerivAt
          (fun z : ℝ =>
            (7 / 2 : ℝ) * z ^ 11)
          (
            (7 / 2 : ℝ) *
              ((11 : ℝ) * y ^ 10)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (7 / 2 : ℝ)
        11
        y

  have h10 :
      HasDerivAt
          (fun z : ℝ =>
            (71 / 20 : ℝ) * z ^ 10)
          (
            (71 / 20 : ℝ) *
              ((10 : ℝ) * y ^ 9)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (71 / 20 : ℝ)
        10
        y

  have h9 :
      HasDerivAt
          (fun z : ℝ =>
            (11 / 9 : ℝ) * z ^ 9)
          (
            (11 / 9 : ℝ) *
              ((9 : ℝ) * y ^ 8)
          )
          y := by
    simpa using
      hasDerivAt_const_mul_pow
        (11 / 9 : ℝ)
        9
        y

  unfold prizcarbonR3CompactTrialPrimitive

  convert
    ((((((hR12.sub hR11).add hR10).sub h12).add h11).sub h10).add h9)
    using 1

  rw [
    prizcarbonR3CompactTrialDensity_expanded
  ]

  ring

theorem prizcarbonR3CompactTrialDensity_continuous
    (r3 : ℝ) :
    Continuous
      (prizcarbonR3CompactTrialDensity r3) := by
  unfold
    prizcarbonR3CompactTrialDensity
    prizcarbonR3CompactQuadraticDensity
    prizcarbonR3CompactPotentialCoefficient
    prizcarbonR3CompactTrialProfile
    prizcarbonR3CompactTrialProfileDerivative

  fun_prop

/-- Exact interval integral of the trial density. -/
theorem prizcarbonR3CompactTrialDensity_integral
    (r3 : ℝ) :
    (∫ y in (0 : ℝ)..1,
      prizcarbonR3CompactTrialDensity r3 y) =
      (3 * r3 + 44) / 7920 := by
  have hIntegrable :
      IntervalIntegrable
        (prizcarbonR3CompactTrialDensity r3)
        MeasureTheory.volume
        0
        1 :=
    (
      prizcarbonR3CompactTrialDensity_continuous
        r3
    ).intervalIntegrable 0 1

  calc
    (∫ y in (0 : ℝ)..1,
        prizcarbonR3CompactTrialDensity r3 y) =
        prizcarbonR3CompactTrialPrimitive r3 1 -
          prizcarbonR3CompactTrialPrimitive r3 0 := by
      exact
        intervalIntegral.integral_eq_sub_of_hasDerivAt
          (
            fun y _ =>
              prizcarbonR3CompactTrialPrimitive_hasDerivAt
                r3
                y
          )
          hIntegrable

    _ = (3 * r3 + 44) / 7920 := by
      norm_num [
        prizcarbonR3CompactTrialPrimitive
      ]
      ring

/--
Reduced dimensional quadratic energy of the explicit profile.

The factor `1 / mass` is the dimensional scaling of the compact-coordinate
form.
-/
def prizcarbonR3CompactTrialQuadraticEnergy
    (r3 mass : ℝ) : ℝ :=
  (
    ∫ y in (0 : ℝ)..1,
      prizcarbonR3CompactTrialDensity r3 y
  ) /
    mass

theorem prizcarbonR3CompactTrialQuadraticEnergy_exact
    (r3 mass : ℝ) :
    prizcarbonR3CompactTrialQuadraticEnergy
        r3
        mass =
      (3 * r3 + 44) /
        (7920 * mass) := by
  unfold
    prizcarbonR3CompactTrialQuadraticEnergy

  rw [
    prizcarbonR3CompactTrialDensity_integral
  ]

  ring

/--
For positive mass and `r3 < -44/3`, the explicit profile has strictly
negative reduced quadratic energy.
-/
theorem prizcarbonR3CompactTrialQuadraticEnergy_neg
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    prizcarbonR3CompactTrialQuadraticEnergy
        r3
        mass <
      0 := by
  rw [
    prizcarbonR3CompactTrialQuadraticEnergy_exact
  ]

  exact
    div_neg_of_neg_of_pos
      (by nlinarith)
      (
        mul_pos
          (by norm_num)
          hMass
      )

/-- The explicit threshold is less restrictive than `r3 < -18`. -/
theorem prizcarbonR3CompactWitnessThreshold_gt_negEighteen :
    -(18 : ℝ) <
      -(44 / 3 : ℝ) := by
  norm_num

/--
Flagship exact compact variational witness.

It proves an exact negative quadratic-form value, not spectral instability.
-/
theorem prizcarbonR3_exactNegativeCompactQuadraticWitness
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    (
      ∀ y : ℝ,
        HasDerivAt
          prizcarbonR3CompactTrialProfile
          (prizcarbonR3CompactTrialProfileDerivative y)
          y
    ) ∧
      prizcarbonR3CompactTrialProfile 0 = 0 ∧
      prizcarbonR3CompactTrialProfile 1 = 0 ∧
      prizcarbonR3CompactTrialQuadraticEnergy
          r3
          mass <
        0 := by
  exact
    ⟨
      prizcarbonR3CompactTrialProfile_hasDerivAt,
      prizcarbonR3CompactTrialProfile_zero,
      prizcarbonR3CompactTrialProfile_one,
      prizcarbonR3CompactTrialQuadraticEnergy_neg
        hMass
        hR3
    ⟩

#check reggeWheelerOddParityMasterField_gaugeInvariant
#check reggeWheelerOddParityGaugeInvariantCarrier

def prizcarbonR3CompactVariationalWitnessStatus :
    String :=
  "EXACT_ENDPOINT_VANISHING_POLYNOMIAL_TRIAL_PROFILE_AND_NEGATIVE_COMPACT_QUADRATIC_ENERGY_FOR_R3_LESS_THAN_NEGATIVE_FORTY_FOUR_OVER_THREE"

def prizcarbonR3CompactVariationalWitnessBoundary :
    String :=
  "EXACT_NONNUMERICAL_QUADRATIC_WITNESS_PROVED_SELF_ADJOINT_TORTOISE_OPERATOR_NEGATIVE_EIGENVALUE_EXPONENTIALLY_GROWING_MODE_AND_COVARIANT_PRIZCARBON_ORIGIN_NOT_PROVED"

end

end Chronos.Frontier
