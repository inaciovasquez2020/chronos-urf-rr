import Mathlib
import Chronos.Frontier.PrizcarbonR3ContinuumVariationalObstruction

namespace Chronos.Frontier

noncomputable section

/-!
# Prizcarbon r3 continuum potential control

For the compact exterior coordinate

  y = 2M / r,

the r3-deformed quadrupole potential is

  V_r3(y)
    =
    y²(1-y)[12 + (r3-6)y] / (8M²).

The absolute tortoise Jacobian is

  |drStar/dy|
    =
    2M / [y²(1-y)].

Away from the two compact-coordinate endpoints, their product simplifies
exactly to

  V_r3(y)|drStar/dy|
    =
    [12 + (r3-6)y] / (4M).

This file proves:

* continuity of the compact potential;
* vanishing at both compact-coordinate endpoints;
* an explicit interior negative-potential witness whenever `r3 < -6`;
* signed and absolute tortoise-density interval integrability;
* exact signed potential area `(r3+18)/(8M)`;
* negative signed area whenever `r3 < -18`;
* the previously established negative continuum variational obstruction for
  `r3 < -44/3`.

This supplies exact potential data required for a later unbounded
Schrodinger-operator realization. It does not claim that the full L2
operator, self-adjointness, essential spectrum, min-max theorem, negative
discrete eigenvalue, or full PDE growing mode have been formalized.
-/

/-- Compact-coordinate r3-deformed Regge-Wheeler potential. -/
def prizcarbonR3CompactExteriorPotential
    (r3 mass y : ℝ) : ℝ :=
  y ^ 2 *
      (1 - y) *
      (12 + (r3 - 6) * y) /
    (8 * mass ^ 2)

/-- Absolute compact-coordinate tortoise Jacobian. -/
def prizcarbonR3CompactTortoiseJacobian
    (mass y : ℝ) : ℝ :=
  2 * mass /
    (y ^ 2 * (1 - y))

/--
Signed potential density after multiplication by the absolute tortoise
Jacobian.
-/
def prizcarbonR3TortoiseSignedPotentialDensity
    (r3 mass y : ℝ) : ℝ :=
  (12 + (r3 - 6) * y) /
    (4 * mass)

/-- Absolute signed-potential density. -/
def prizcarbonR3TortoiseAbsolutePotentialDensity
    (r3 mass y : ℝ) : ℝ :=
  abs
    (
      prizcarbonR3TortoiseSignedPotentialDensity
        r3
        mass
        y
    )

/--
Explicit interior compact-coordinate point at which the linear potential
factor is negative when `r3 < -6`.
-/
def prizcarbonR3NegativePocketWitness
    (r3 : ℝ) : ℝ :=
  (18 - r3) /
    (2 * (6 - r3))

/-- Primitive of the signed tortoise potential density. -/
def prizcarbonR3TortoiseSignedPotentialPrimitive
    (r3 mass y : ℝ) : ℝ :=
  (3 / mass) * y +
    ((r3 - 6) / (8 * mass)) *
      y ^ 2

/-- The compact potential is continuous. -/
theorem prizcarbonR3CompactExteriorPotential_continuous
    (r3 mass : ℝ) :
    Continuous
      (
        prizcarbonR3CompactExteriorPotential
          r3
          mass
      ) := by
  unfold prizcarbonR3CompactExteriorPotential
  fun_prop

/-- The compact potential vanishes at spatial infinity, `y = 0`. -/
theorem prizcarbonR3CompactExteriorPotential_zero
    (r3 mass : ℝ) :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        0 =
      0 := by
  norm_num [
    prizcarbonR3CompactExteriorPotential
  ]

/-- The compact potential vanishes at the horizon, `y = 1`. -/
theorem prizcarbonR3CompactExteriorPotential_one
    (r3 mass : ℝ) :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        1 =
      0 := by
  norm_num [
    prizcarbonR3CompactExteriorPotential
  ]

/--
Away from the endpoints, compact potential times tortoise Jacobian equals
the signed tortoise density.
-/
theorem
    prizcarbonR3CompactPotential_mul_tortoiseJacobian
    {r3 mass y : ℝ}
    (hMass : mass ≠ 0)
    (hyZero : y ≠ 0)
    (hyOne : y ≠ 1) :
    prizcarbonR3CompactExteriorPotential
          r3
          mass
          y *
        prizcarbonR3CompactTortoiseJacobian
          mass
          y =
      prizcarbonR3TortoiseSignedPotentialDensity
        r3
        mass
        y := by
  have hySquare :
      y ^ 2 ≠ 0 :=
    pow_ne_zero
      2
      hyZero

  have hOneSub :
      1 - y ≠ 0 :=
    sub_ne_zero.mpr
      (
        Ne.symm
          hyOne
      )

  unfold
    prizcarbonR3CompactExteriorPotential
    prizcarbonR3CompactTortoiseJacobian
    prizcarbonR3TortoiseSignedPotentialDensity

  field_simp [
    hMass,
    hySquare,
    hOneSub
  ]

  ring

/-- The explicit negative-pocket witness belongs to `(0,1)` for `r3 < -6`. -/
theorem prizcarbonR3NegativePocketWitness_mem_Ioo
    {r3 : ℝ}
    (hR3 : r3 < -(6 : ℝ)) :
    prizcarbonR3NegativePocketWitness r3 ∈
      Set.Ioo (0 : ℝ) 1 := by
  have hBaseDenominator :
      0 < 6 - r3 := by
    linarith

  have hDenominator :
      0 <
        2 * (6 - r3) :=
    mul_pos
      (by norm_num)
      hBaseDenominator

  have hNumerator :
      0 <
        18 - r3 := by
    linarith

  have hNumeratorLt :
      18 - r3 <
        2 * (6 - r3) := by
    nlinarith

  constructor

  · unfold prizcarbonR3NegativePocketWitness

    exact
      div_pos
        hNumerator
        hDenominator

  · unfold prizcarbonR3NegativePocketWitness

    apply
      (
        div_lt_iff₀
          hDenominator
      ).2

    simpa using hNumeratorLt

/--
At the explicit witness, the linear potential factor is exactly
`(r3+6)/2`.
-/
theorem
    prizcarbonR3NegativePocketWitness_linearFactor
    {r3 : ℝ}
    (hR3 : r3 < -(6 : ℝ)) :
    12 +
          (r3 - 6) *
            prizcarbonR3NegativePocketWitness
              r3 =
      (r3 + 6) / 2 := by
  have hDenominator :
      6 - r3 ≠ 0 :=
    ne_of_gt
      (
        by
          linarith
      )

  unfold prizcarbonR3NegativePocketWitness

  field_simp [
    hDenominator
  ]

  ring

/--
For positive mass and `r3 < -6`, the compact potential has a strictly
negative interior point.
-/
theorem
    prizcarbonR3CompactExteriorPotential_negativePocket
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(6 : ℝ)) :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        (
          prizcarbonR3NegativePocketWitness
            r3
        ) <
      0 := by
  have hWitness :=
    prizcarbonR3NegativePocketWitness_mem_Ioo
      hR3

  have hYSquared :
      0 <
        (
          prizcarbonR3NegativePocketWitness
            r3
        ) ^ 2 :=
    pow_pos
      hWitness.1
      2

  have hOneSub :
      0 <
        1 -
          prizcarbonR3NegativePocketWitness
            r3 :=
    sub_pos.mpr
      hWitness.2

  have hLinearFactor :
      12 +
            (r3 - 6) *
              prizcarbonR3NegativePocketWitness
                r3 <
        0 := by
    rw [
      prizcarbonR3NegativePocketWitness_linearFactor
        hR3
    ]

    linarith

  have hNumerator :
      (
        (
          prizcarbonR3NegativePocketWitness
            r3
        ) ^ 2
      ) *
          (
            1 -
              prizcarbonR3NegativePocketWitness
                r3
          ) *
          (
            12 +
              (r3 - 6) *
                prizcarbonR3NegativePocketWitness
                  r3
          ) <
        0 :=
    mul_neg_of_pos_of_neg
      (
        mul_pos
          hYSquared
          hOneSub
      )
      hLinearFactor

  have hDenominator :
      0 <
        8 * mass ^ 2 :=
    mul_pos
      (by norm_num)
      (
        pow_pos
          hMass
          2
      )

  unfold prizcarbonR3CompactExteriorPotential

  exact
    div_neg_of_neg_of_pos
      hNumerator
      hDenominator

/-- The signed tortoise density is continuous. -/
theorem
    prizcarbonR3TortoiseSignedPotentialDensity_continuous
    (r3 mass : ℝ) :
    Continuous
      (
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
      ) := by
  unfold prizcarbonR3TortoiseSignedPotentialDensity
  fun_prop

/-- The absolute tortoise density is continuous. -/
theorem
    prizcarbonR3TortoiseAbsolutePotentialDensity_continuous
    (r3 mass : ℝ) :
    Continuous
      (
        prizcarbonR3TortoiseAbsolutePotentialDensity
          r3
          mass
      ) := by
  simpa [
    prizcarbonR3TortoiseAbsolutePotentialDensity
  ] using
    (
      prizcarbonR3TortoiseSignedPotentialDensity_continuous
        r3
        mass
    ).abs

/-- The signed tortoise density is interval-integrable. -/
theorem
    prizcarbonR3TortoiseSignedPotentialDensity_intervalIntegrable
    (r3 mass : ℝ) :
    IntervalIntegrable
      (
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
      )
      MeasureTheory.volume
      0
      1 :=
  (
    prizcarbonR3TortoiseSignedPotentialDensity_continuous
      r3
      mass
  ).intervalIntegrable
    (μ := MeasureTheory.volume)
    0
    1

/-- The absolute tortoise density is interval-integrable. -/
theorem
    prizcarbonR3TortoiseAbsolutePotentialDensity_intervalIntegrable
    (r3 mass : ℝ) :
    IntervalIntegrable
      (
        prizcarbonR3TortoiseAbsolutePotentialDensity
          r3
          mass
      )
      MeasureTheory.volume
      0
      1 :=
  (
    prizcarbonR3TortoiseAbsolutePotentialDensity_continuous
      r3
      mass
  ).intervalIntegrable
    (μ := MeasureTheory.volume)
    0
    1

/-- The primitive differentiates to the signed tortoise density. -/
theorem
    prizcarbonR3TortoiseSignedPotentialPrimitive_hasDerivAt
    (r3 mass y : ℝ) :
    HasDerivAt
      (
        prizcarbonR3TortoiseSignedPotentialPrimitive
          r3
          mass
      )
      (
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
          y
      )
      y := by
  have hLinear :
      HasDerivAt
        (
          fun z : ℝ =>
            (3 / mass) * z
        )
        (3 / mass)
        y := by
    simpa using
      (
        hasDerivAt_id y
      ).const_mul
        (3 / mass)

  have hQuadratic :
      HasDerivAt
        (
          fun z : ℝ =>
            ((r3 - 6) / (8 * mass)) *
              z ^ 2
        )
        (
          ((r3 - 6) / (8 * mass)) *
            ((2 : ℝ) * y)
        )
        y := by
    simpa [
      id,
      mul_assoc
    ] using
      (
        (
          hasDerivAt_id y
        ).pow 2
      ).const_mul
        (
          (r3 - 6) /
            (8 * mass)
        )

  unfold
    prizcarbonR3TortoiseSignedPotentialPrimitive
    prizcarbonR3TortoiseSignedPotentialDensity

  convert
    hLinear.add hQuadratic
    using 1

  all_goals ring

/-- Exact signed tortoise-coordinate potential area. -/
theorem
    prizcarbonR3TortoiseSignedPotentialDensity_integral
    {r3 mass : ℝ}
    (hMass : mass ≠ 0) :
    (
      ∫ y in (0 : ℝ)..1,
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
          y
    ) =
      (r3 + 18) /
        (8 * mass) := by
  have hIntegrable :
      IntervalIntegrable
        (
          prizcarbonR3TortoiseSignedPotentialDensity
            r3
            mass
        )
        MeasureTheory.volume
        0
        1 :=
    prizcarbonR3TortoiseSignedPotentialDensity_intervalIntegrable
      r3
      mass

  calc
    (
      ∫ y in (0 : ℝ)..1,
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
          y
    ) =
        prizcarbonR3TortoiseSignedPotentialPrimitive
            r3
            mass
            1 -
          prizcarbonR3TortoiseSignedPotentialPrimitive
            r3
            mass
            0 := by
      exact
        intervalIntegral.integral_eq_sub_of_hasDerivAt
          (
            fun y _ =>
              prizcarbonR3TortoiseSignedPotentialPrimitive_hasDerivAt
                r3
                mass
                y
          )
          hIntegrable

    _ = (r3 + 18) / (8 * mass) := by
      norm_num [
        prizcarbonR3TortoiseSignedPotentialPrimitive
      ]

      field_simp [
        hMass
      ]

      ring

/-- The exact signed potential area is negative when `r3 < -18`. -/
theorem
    prizcarbonR3TortoiseSignedPotentialDensity_integral_neg
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(18 : ℝ)) :
    (
      ∫ y in (0 : ℝ)..1,
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
          y
    ) <
      0 := by
  rw [
    prizcarbonR3TortoiseSignedPotentialDensity_integral
      (
        ne_of_gt
          hMass
      )
  ]

  exact
    div_neg_of_neg_of_pos
      (by linarith)
      (
        mul_pos
          (by norm_num)
          hMass
      )

/--
Exact continuum-potential control certificate at the variational threshold
`r3 < -44/3`.
-/
structure PrizcarbonR3ContinuumPotentialControlCertificate
    (r3 mass : ℝ) : Prop where
  continuumVariationalObstruction :
    PrizcarbonR3ContinuumVariationalObstructionCertificate
      r3
      mass

  compactPotentialContinuous :
    Continuous
      (
        prizcarbonR3CompactExteriorPotential
          r3
          mass
      )

  compactPotentialZeroAtInfinity :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        0 =
      0

  compactPotentialZeroAtHorizon :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        1 =
      0

  negativePocketWitnessInterior :
    prizcarbonR3NegativePocketWitness r3 ∈
      Set.Ioo (0 : ℝ) 1

  negativePocket :
    prizcarbonR3CompactExteriorPotential
        r3
        mass
        (
          prizcarbonR3NegativePocketWitness
            r3
        ) <
      0

  signedTortoiseDensityIntegrable :
    IntervalIntegrable
      (
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
      )
      MeasureTheory.volume
      0
      1

  absoluteTortoiseDensityIntegrable :
    IntervalIntegrable
      (
        prizcarbonR3TortoiseAbsolutePotentialDensity
          r3
          mass
      )
      MeasureTheory.volume
      0
      1

  signedAreaExact :
    (
      ∫ y in (0 : ℝ)..1,
        prizcarbonR3TortoiseSignedPotentialDensity
          r3
          mass
          y
    ) =
      (r3 + 18) /
        (8 * mass)

/--
Flagship exact continuum-potential theorem.

For positive mass and `r3 < -44/3`, the continuum variational obstruction
holds, the compact potential is continuous and endpoint-vanishing, an
explicit interior negative pocket exists, the signed and absolute tortoise
densities are integrable, and the signed area is exact.
-/
theorem prizcarbonR3_exactContinuumPotentialControl
    {r3 mass : ℝ}
    (hMass : 0 < mass)
    (hR3 : r3 < -(44 / 3 : ℝ)) :
    PrizcarbonR3ContinuumPotentialControlCertificate
      r3
      mass := by
  have hR3Six :
      r3 < -(6 : ℝ) := by
    nlinarith

  exact
    {
      continuumVariationalObstruction :=
        prizcarbonR3_exactContinuumVariationalObstruction
          hMass
          hR3

      compactPotentialContinuous :=
        prizcarbonR3CompactExteriorPotential_continuous
          r3
          mass

      compactPotentialZeroAtInfinity :=
        prizcarbonR3CompactExteriorPotential_zero
          r3
          mass

      compactPotentialZeroAtHorizon :=
        prizcarbonR3CompactExteriorPotential_one
          r3
          mass

      negativePocketWitnessInterior :=
        prizcarbonR3NegativePocketWitness_mem_Ioo
          hR3Six

      negativePocket :=
        prizcarbonR3CompactExteriorPotential_negativePocket
          hMass
          hR3Six

      signedTortoiseDensityIntegrable :=
        prizcarbonR3TortoiseSignedPotentialDensity_intervalIntegrable
          r3
          mass

      absoluteTortoiseDensityIntegrable :=
        prizcarbonR3TortoiseAbsolutePotentialDensity_intervalIntegrable
          r3
          mass

      signedAreaExact :=
        prizcarbonR3TortoiseSignedPotentialDensity_integral
          (
            ne_of_gt
              hMass
          )
    }

def prizcarbonR3ContinuumPotentialControlStatus :
    String :=
  "EXACT_COMPACT_POTENTIAL_ENDPOINT_DECAY_EXPLICIT_NEGATIVE_POCKET_TORTOISE_DENSITY_INTEGRABILITY_SIGNED_AREA_AND_NEGATIVE_CONTINUUM_FORM_PROVED"

def prizcarbonR3ContinuumPotentialControlBoundary :
    String :=
  "FULL_UNBOUNDED_L2_REGGE_WHEELER_OPERATOR_SELF_ADJOINT_REALIZATION_ESSENTIAL_SPECTRUM_MIN_MAX_NEGATIVE_DISCRETE_EIGENVALUE_FULL_PDE_GROWING_MODE_AND_COVARIANT_PRIZCARBON_ORIGIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
