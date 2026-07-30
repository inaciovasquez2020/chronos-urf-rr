import Mathlib
import Chronos.Frontier.PrizcarbonR3CompactVariationalWitness

namespace Chronos.Frontier

noncomputable section

/-!
# Prizcarbon r3 one-mode Galerkin instability

The compact variational witness supplies the exact quadratic energy

  Q_r3[Psi] = (3 r3 + 44) / (7920 M)

for the trial profile

  Psi(y) = y^4 (1-y).

This module computes the exact tortoise-coordinate squared norm

  ||Psi||^2 = M / 28,

and the corresponding one-mode Rayleigh eigenvalue

  lambda_G = 7 (3 r3 + 44) / (1980 M^2).

For positive mass and `r3 < -44/3`, this eigenvalue is strictly negative.
The projected one-dimensional operator has an explicit eigenvector and an
explicit exponentially growing solution.

This is an exact theorem for the one-mode Galerkin projection. It is not an
eigenvalue theorem for the full infinite-dimensional Regge-Wheeler operator.
-/

/-- Tortoise-coordinate norm density of the compact trial profile. -/
def prizcarbonR3GalerkinNormDensity
    (mass y : ℝ) : ℝ :=
  2 * mass * (y ^ 6 - y ^ 7)

/-- Polynomial primitive of the norm density. -/
def prizcarbonR3GalerkinNormPrimitive
    (mass y : ℝ) : ℝ :=
  (2 * mass / 7) * y ^ 7 -
    (mass / 4) * y ^ 8

private theorem
    prizcarbonR3Galerkin_hasDerivAt_const_mul_pow
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

theorem prizcarbonR3GalerkinNormPrimitive_hasDerivAt
    (mass y : ℝ) :
    HasDerivAt
        (prizcarbonR3GalerkinNormPrimitive mass)
        (prizcarbonR3GalerkinNormDensity mass y)
        y := by
  have hSeven :
      HasDerivAt
          (fun z : ℝ =>
            (2 * mass / 7) * z ^ 7)
          (
            (2 * mass / 7) *
              ((7 : ℝ) * y ^ 6)
          )
          y := by
    simpa using
      prizcarbonR3Galerkin_hasDerivAt_const_mul_pow
        (2 * mass / 7)
        7
        y

  have hEight :
      HasDerivAt
          (fun z : ℝ =>
            (mass / 4) * z ^ 8)
          (
            (mass / 4) *
              ((8 : ℝ) * y ^ 7)
          )
          y := by
    simpa using
      prizcarbonR3Galerkin_hasDerivAt_const_mul_pow
        (mass / 4)
        8
        y

  unfold
    prizcarbonR3GalerkinNormPrimitive
    prizcarbonR3GalerkinNormDensity

  convert hSeven.sub hEight using 1
  all_goals ring

theorem prizcarbonR3GalerkinNormDensity_continuous
    (mass : ℝ) :
    Continuous
      (prizcarbonR3GalerkinNormDensity mass) := by
  unfold prizcarbonR3GalerkinNormDensity
  fun_prop

/-- Exact tortoise-coordinate squared norm of the trial profile. -/
def prizcarbonR3GalerkinNormSquared
    (mass : ℝ) : ℝ :=
  ∫ y in (0 : ℝ)..1,
    prizcarbonR3GalerkinNormDensity mass y

theorem prizcarbonR3GalerkinNormSquared_exact
    (mass : ℝ) :
    prizcarbonR3GalerkinNormSquared mass =
      mass / 28 := by
  have hIntegrable :
      IntervalIntegrable
        (prizcarbonR3GalerkinNormDensity mass)
        MeasureTheory.volume
        0
        1 :=
    (
      prizcarbonR3GalerkinNormDensity_continuous
        mass
    ).intervalIntegrable 0 1

  unfold prizcarbonR3GalerkinNormSquared

  calc
    (∫ y in (0 : ℝ)..1,
        prizcarbonR3GalerkinNormDensity mass y) =
        prizcarbonR3GalerkinNormPrimitive mass 1 -
          prizcarbonR3GalerkinNormPrimitive mass 0 := by
      exact
        intervalIntegral.integral_eq_sub_of_hasDerivAt
          (
            fun y _ =>
              prizcarbonR3GalerkinNormPrimitive_hasDerivAt
                mass
                y
          )
          hIntegrable

    _ = mass / 28 := by
      norm_num [
        prizcarbonR3GalerkinNormPrimitive
      ]
      ring

theorem prizcarbonR3GalerkinNormSquared_pos
    {mass : ℝ}
    (hMass : 0 < mass) :
    0 <
      prizcarbonR3GalerkinNormSquared mass := by
  rw [
    prizcarbonR3GalerkinNormSquared_exact
  ]

  exact
    div_pos
      hMass
      (by norm_num)

/-- Exact one-mode Rayleigh eigenvalue. -/
def prizcarbonR3GalerkinEigenvalue
    (r3 mass : ℝ) : ℝ :=
  7 * (3 * r3 + 44) /
    (1980 * mass ^ 2)

/--
The compact quadratic energy equals the Galerkin eigenvalue multiplied by the
exact trial-profile norm.
-/
theorem
    prizcarbonR3CompactTrialEnergy_eq_galerkinEigenvalue_mul_norm
    {r3 mass : ℝ}
    (hMass : mass ≠ 0) :
    prizcarbonR3CompactTrialQuadraticEnergy
        r3
        mass =
      prizcarbonR3GalerkinEigenvalue
          r3
          mass *
        prizcarbonR3GalerkinNormSquared
          mass := by
  rw [
    prizcarbonR3CompactTrialQuadraticEnergy_exact,
    prizcarbonR3GalerkinNormSquared_exact
  ]

  unfold prizcarbonR3GalerkinEigenvalue

  field_simp [hMass]
  ring

/-- The exact Galerkin eigenvalue is negative below the witness threshold. -/
theorem prizcarbonR3GalerkinEigenvalue_neg
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    prizcarbonR3GalerkinEigenvalue
        r3
        mass <
      0 := by
  have hNumerator :
      3 * r3 + 44 <
        0 := by
    nlinarith

  have hScaledNumerator :
      7 * (3 * r3 + 44) <
        0 :=
    mul_neg_of_pos_of_neg
      (by norm_num)
      hNumerator

  have hMassSquared :
      0 < mass ^ 2 :=
    pow_pos hMass 2

  have hDenominator :
      0 <
        1980 * mass ^ 2 :=
    mul_pos
      (by norm_num)
      hMassSquared

  unfold prizcarbonR3GalerkinEigenvalue

  exact
    div_neg_of_neg_of_pos
      hScaledNumerator
      hDenominator

/-- One-dimensional Galerkin projection. -/
def prizcarbonR3GalerkinOperator
    (r3 mass : ℝ) :
    Module.End ℝ ℝ :=
  prizcarbonR3GalerkinEigenvalue
      r3
      mass •
    (LinearMap.id : Module.End ℝ ℝ)

@[simp]
theorem prizcarbonR3GalerkinOperator_apply
    (r3 mass amplitude : ℝ) :
    prizcarbonR3GalerkinOperator
        r3
        mass
        amplitude =
      prizcarbonR3GalerkinEigenvalue
          r3
          mass *
        amplitude := by
  simp [
    prizcarbonR3GalerkinOperator
  ]

/-- Graph of the one-mode operator. -/
def prizcarbonR3GalerkinOperatorGraph
    (r3 mass : ℝ) :
    Set (ℝ × ℝ) :=
  {
    pair |
      prizcarbonR3GalerkinOperator
          r3
          mass
          pair.1 =
        pair.2
  }

/-- The one-dimensional operator graph is closed. -/
theorem prizcarbonR3GalerkinOperatorGraph_isClosed
    (r3 mass : ℝ) :
    IsClosed
      (
        prizcarbonR3GalerkinOperatorGraph
          r3
          mass
      ) := by
  unfold prizcarbonR3GalerkinOperatorGraph

  apply isClosed_eq

  · fun_prop

  · fun_prop

/-- The amplitude `1` is an exact eigenvector. -/
theorem
    prizcarbonR3GalerkinOperator_one_hasEigenvector
    (r3 mass : ℝ) :
    (
      prizcarbonR3GalerkinOperator
        r3
        mass
    ).HasEigenvector
      (
        prizcarbonR3GalerkinEigenvalue
          r3
          mass
      )
      1 := by
  rw [
    Module.End.hasEigenvector_iff
  ]

  constructor

  · rw [
      Module.End.mem_eigenspace_iff
    ]

    simp [
      prizcarbonR3GalerkinOperator
    ]

  · norm_num

/-- The Rayleigh value is an actual eigenvalue. -/
theorem
    prizcarbonR3GalerkinOperator_hasEigenvalue
    (r3 mass : ℝ) :
    (
      prizcarbonR3GalerkinOperator
        r3
        mass
    ).HasEigenvalue
      (
        prizcarbonR3GalerkinEigenvalue
          r3
          mass
      ) := by
  exact
    Module.End.hasEigenvalue_of_hasEigenvector
      (
        prizcarbonR3GalerkinOperator_one_hasEigenvector
          r3
          mass
      )

/-- Exact existence of a negative Galerkin eigenvalue. -/
theorem
    prizcarbonR3GalerkinOperator_exists_negativeEigenvalue
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    ∃ eigenvalue : ℝ,
      eigenvalue < 0 ∧
      (
        prizcarbonR3GalerkinOperator
          r3
          mass
      ).HasEigenvalue eigenvalue := by
  exact
    ⟨
      prizcarbonR3GalerkinEigenvalue
        r3
        mass,
      prizcarbonR3GalerkinEigenvalue_neg
        hMass
        hR3,
      prizcarbonR3GalerkinOperator_hasEigenvalue
        r3
        mass
    ⟩

/-- Positive growth rate associated with the negative eigenvalue. -/
def prizcarbonR3GalerkinGrowthRate
    (r3 mass : ℝ) : ℝ :=
  Real.sqrt
    (
      -
        prizcarbonR3GalerkinEigenvalue
          r3
          mass
    )

theorem prizcarbonR3GalerkinGrowthRate_pos
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    0 <
      prizcarbonR3GalerkinGrowthRate
        r3
        mass := by
  unfold prizcarbonR3GalerkinGrowthRate

  rw [
    Real.sqrt_pos
  ]

  exact
    neg_pos.mpr
      (
        prizcarbonR3GalerkinEigenvalue_neg
          hMass
          hR3
      )

theorem prizcarbonR3GalerkinGrowthRate_sq
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    prizcarbonR3GalerkinGrowthRate
          r3
          mass ^ 2 =
      -
        prizcarbonR3GalerkinEigenvalue
          r3
          mass := by
  unfold prizcarbonR3GalerkinGrowthRate

  exact
    Real.sq_sqrt
      (
        le_of_lt
          (
            neg_pos.mpr
              (
                prizcarbonR3GalerkinEigenvalue_neg
                  hMass
                  hR3
              )
          )
      )

/-- Explicit exponentially growing amplitude. -/
def prizcarbonR3GalerkinGrowthMode
    (r3 mass t : ℝ) : ℝ :=
  Real.exp
    (
      prizcarbonR3GalerkinGrowthRate
          r3
          mass *
        t
    )

/-- First derivative of the growth mode. -/
def prizcarbonR3GalerkinGrowthVelocity
    (r3 mass t : ℝ) : ℝ :=
  prizcarbonR3GalerkinGrowthRate
      r3
      mass *
    prizcarbonR3GalerkinGrowthMode
      r3
      mass
      t

theorem prizcarbonR3GalerkinGrowthMode_zero
    (r3 mass : ℝ) :
    prizcarbonR3GalerkinGrowthMode
        r3
        mass
        0 =
      1 := by
  simp [
    prizcarbonR3GalerkinGrowthMode
  ]

theorem prizcarbonR3GalerkinGrowthMode_hasDerivAt
    (r3 mass t : ℝ) :
    HasDerivAt
      (
        prizcarbonR3GalerkinGrowthMode
          r3
          mass
      )
      (
        prizcarbonR3GalerkinGrowthVelocity
          r3
          mass
          t
      )
      t := by
  have hLinear :
      HasDerivAt
        (
          fun s : ℝ =>
            prizcarbonR3GalerkinGrowthRate
                r3
                mass *
              s
        )
        (
          prizcarbonR3GalerkinGrowthRate
            r3
            mass
        )
        t := by
    simpa using
      (
        hasDerivAt_id t
      ).const_mul
        (
          prizcarbonR3GalerkinGrowthRate
            r3
            mass
        )

  change
    HasDerivAt
      (
        fun s : ℝ =>
          Real.exp
            (
              prizcarbonR3GalerkinGrowthRate
                  r3
                  mass *
                s
            )
      )
      (
        prizcarbonR3GalerkinGrowthRate
            r3
            mass *
          Real.exp
            (
              prizcarbonR3GalerkinGrowthRate
                  r3
                  mass *
                t
            )
      )
      t

  simpa [
    mul_comm,
    mul_left_comm,
    mul_assoc
  ] using
    hLinear.exp

theorem
    prizcarbonR3GalerkinGrowthVelocity_hasDerivAt
    (r3 mass t : ℝ) :
    HasDerivAt
      (
        prizcarbonR3GalerkinGrowthVelocity
          r3
          mass
      )
      (
        prizcarbonR3GalerkinGrowthRate
              r3
              mass ^ 2 *
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
            t
      )
      t := by
  simpa [
    prizcarbonR3GalerkinGrowthVelocity,
    pow_two,
    mul_assoc
  ] using
    (
      prizcarbonR3GalerkinGrowthMode_hasDerivAt
        r3
        mass
        t
    ).const_mul
      (
        prizcarbonR3GalerkinGrowthRate
          r3
          mass
      )

theorem
    prizcarbonR3GalerkinGrowthVelocity_hasDerivAt_negEigenvalue
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ))
    (t : ℝ) :
    HasDerivAt
      (
        prizcarbonR3GalerkinGrowthVelocity
          r3
          mass
      )
      (
        -
            prizcarbonR3GalerkinEigenvalue
              r3
              mass *
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
            t
      )
      t := by
  have hDerivative :=
    prizcarbonR3GalerkinGrowthVelocity_hasDerivAt
      r3
      mass
      t

  rw [
    prizcarbonR3GalerkinGrowthRate_sq
      hMass
      hR3
  ] at hDerivative

  exact hDerivative

/-- The exponential mode solves the projected wave equation. -/
theorem prizcarbonR3GalerkinGrowthMode_waveEquation
    {r3 mass : ℝ}
    (t : ℝ) :
    -
          prizcarbonR3GalerkinEigenvalue
            r3
            mass *
        prizcarbonR3GalerkinGrowthMode
          r3
          mass
          t +
      prizcarbonR3GalerkinOperator
        r3
        mass
        (
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
            t
        ) =
      0 := by
  rw [
    prizcarbonR3GalerkinOperator_apply
  ]

  ring

/-- The mode is strictly above its initial amplitude for positive time. -/
theorem prizcarbonR3GalerkinGrowthMode_gt_one
    {r3 mass t : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ))
    (hTime : 0 < t) :
    1 <
      prizcarbonR3GalerkinGrowthMode
        r3
        mass
        t := by
  unfold prizcarbonR3GalerkinGrowthMode

  rw [
    Real.one_lt_exp_iff
  ]

  exact
    mul_pos
      (
        prizcarbonR3GalerkinGrowthRate_pos
          hMass
          hR3
      )
      hTime

/-- Exact certificate for the one-mode instability. -/
structure PrizcarbonR3GalerkinInstabilityCertificate
    (r3 mass : ℝ) : Prop where
  rayleighIdentity :
    prizcarbonR3CompactTrialQuadraticEnergy
        r3
        mass =
      prizcarbonR3GalerkinEigenvalue
          r3
          mass *
        prizcarbonR3GalerkinNormSquared
          mass
  normPositive :
    0 <
      prizcarbonR3GalerkinNormSquared
        mass
  eigenvalueNegative :
    prizcarbonR3GalerkinEigenvalue
        r3
        mass <
      0
  operatorGraphClosed :
    IsClosed
      (
        prizcarbonR3GalerkinOperatorGraph
          r3
          mass
      )
  operatorHasEigenvalue :
    (
      prizcarbonR3GalerkinOperator
        r3
        mass
    ).HasEigenvalue
      (
        prizcarbonR3GalerkinEigenvalue
          r3
          mass
      )
  growthRatePositive :
    0 <
      prizcarbonR3GalerkinGrowthRate
        r3
        mass
  modeInitial :
    prizcarbonR3GalerkinGrowthMode
        r3
        mass
        0 =
      1
  modeDerivative :
    ∀ t : ℝ,
      HasDerivAt
        (
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
        )
        (
          prizcarbonR3GalerkinGrowthVelocity
            r3
            mass
            t
        )
        t
  velocityDerivative :
    ∀ t : ℝ,
      HasDerivAt
        (
          prizcarbonR3GalerkinGrowthVelocity
            r3
            mass
        )
        (
          -
              prizcarbonR3GalerkinEigenvalue
                r3
                mass *
            prizcarbonR3GalerkinGrowthMode
              r3
              mass
              t
        )
        t
  projectedWaveEquation :
    ∀ t : ℝ,
      -
            prizcarbonR3GalerkinEigenvalue
              r3
              mass *
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
            t +
        prizcarbonR3GalerkinOperator
          r3
          mass
          (
            prizcarbonR3GalerkinGrowthMode
              r3
              mass
              t
          ) =
        0
  strictPositiveTimeGrowth :
    ∀ t : ℝ,
      0 < t →
        1 <
          prizcarbonR3GalerkinGrowthMode
            r3
            mass
            t

/--
For positive mass and `r3 < -44/3`, the derived one-mode Galerkin operator
has a negative eigenvalue and an explicit exponentially growing solution.
-/
theorem
    prizcarbonR3Galerkin_negativeEigenvalue_and_exponentialInstability
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    PrizcarbonR3GalerkinInstabilityCertificate
      r3
      mass := by
  exact
    {
      rayleighIdentity :=
        prizcarbonR3CompactTrialEnergy_eq_galerkinEigenvalue_mul_norm
          hMass.ne'
      normPositive :=
        prizcarbonR3GalerkinNormSquared_pos
          hMass
      eigenvalueNegative :=
        prizcarbonR3GalerkinEigenvalue_neg
          hMass
          hR3
      operatorGraphClosed :=
        prizcarbonR3GalerkinOperatorGraph_isClosed
          r3
          mass
      operatorHasEigenvalue :=
        prizcarbonR3GalerkinOperator_hasEigenvalue
          r3
          mass
      growthRatePositive :=
        prizcarbonR3GalerkinGrowthRate_pos
          hMass
          hR3
      modeInitial :=
        prizcarbonR3GalerkinGrowthMode_zero
          r3
          mass
      modeDerivative :=
        prizcarbonR3GalerkinGrowthMode_hasDerivAt
          r3
          mass
      velocityDerivative :=
        prizcarbonR3GalerkinGrowthVelocity_hasDerivAt_negEigenvalue
          hMass
          hR3
      projectedWaveEquation :=
        prizcarbonR3GalerkinGrowthMode_waveEquation
      strictPositiveTimeGrowth :=
        fun t hTime =>
          prizcarbonR3GalerkinGrowthMode_gt_one
            hMass
            hR3
            hTime
    }

def prizcarbonR3GalerkinInstabilityStatus :
    String :=
  "EXACT_ONE_MODE_GALERKIN_NORM_RAYLEIGH_NEGATIVE_EIGENVALUE_CLOSED_GRAPH_AND_EXPONENTIALLY_GROWING_PROJECTED_MODE_PROVED_FOR_R3_LESS_THAN_NEGATIVE_FORTY_FOUR_OVER_THREE"

def prizcarbonR3GalerkinInstabilityBoundary :
    String :=
  "EXACT_ONE_MODE_GALERKIN_INSTABILITY_PROVED_FULL_INFINITE_DIMENSIONAL_REGGE_WHEELER_OPERATOR_SELF_ADJOINT_REALIZATION_NEGATIVE_EIGENVALUE_AND_COVARIANT_PRIZCARBON_ORIGIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
