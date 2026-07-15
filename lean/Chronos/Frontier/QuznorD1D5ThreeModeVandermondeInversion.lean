import Mathlib

namespace Chronos.Frontier

theorem quznor_three_mode_vandermonde_inversion
    (S2 S3 S4 : ℝ) :
    let μ0 := S2 + S3 + S4
    let μ1 := 4 * S2 + 9 * S3 + 16 * S4
    let μ2 := 16 * S2 + 81 * S3 + 256 * S4
    S2 =
        (12 / 5 : ℝ) * μ0
          - (5 / 12 : ℝ) * μ1
          + (1 / 60 : ℝ) * μ2 ∧
    S3 =
        -(64 / 35 : ℝ) * μ0
          + (4 / 7 : ℝ) * μ1
          - (1 / 35 : ℝ) * μ2 ∧
    S4 =
        (3 / 7 : ℝ) * μ0
          - (13 / 84 : ℝ) * μ1
          + (1 / 84 : ℝ) * μ2 := by
  dsimp
  constructor
  · ring
  constructor
  · ring
  · ring


/--
The first three asymptotic coefficient data exactly isolate the
three mode amplitudes associated with weights `2`, `3`, and `4`.
-/
theorem quznorThreeModeAsymptoticCoefficientIsolation
    (S2 S3 S4 A0 A1 A2 : ℝ)
    (hA0 : A0 = S2 + S3 + S4)
    (hA1 : A1 = 4 * S2 + 9 * S3 + 16 * S4)
    (hA2 : A2 = 16 * S2 + 81 * S3 + 256 * S4) :
    S2 =
        (12 / 5 : ℝ) * A0 -
          (5 / 12 : ℝ) * A1 +
          (1 / 60 : ℝ) * A2 ∧
      S3 =
        -(64 / 35 : ℝ) * A0 +
          (4 / 7 : ℝ) * A1 -
          (1 / 35 : ℝ) * A2 ∧
      S4 =
        (3 / 7 : ℝ) * A0 -
          (13 / 84 : ℝ) * A1 +
          (1 / 84 : ℝ) * A2 := by
  subst A0
  subst A1
  subst A2
  constructor
  · ring
  constructor <;> ring


/--
Concrete three-mode radial asymptotic field with inverse-radius modes
`r⁻²`, `r⁻³`, and `r⁻⁴`.
-/
noncomputable def quznorThreeModeAsymptoticField
    (S2 S3 S4 r : ℝ) : ℝ :=
  S2 / r ^ 2 +
    S3 / r ^ 3 +
    S4 / r ^ 4


/--
Evaluation of the concrete three-mode asymptotic field at unit radius
recovers the zeroth asymptotic coefficient.
-/
theorem quznorThreeModeAsymptoticField_at_one_eq_A0
    (S2 S3 S4 A0 : ℝ)
    (hA0 : A0 = S2 + S3 + S4) :
    quznorThreeModeAsymptoticField S2 S3 S4 1 = A0 := by
  simpa [quznorThreeModeAsymptoticField] using hA0.symm


/--
At unit radius, the modewise squared-Euler expression has weights
`2²`, `3²`, and `4²`, and therefore recovers `A1`.
-/
theorem quznorThreeModeSquaredEulerCoefficient_at_one_eq_A1
    (S2 S3 S4 A1 : ℝ)
    (hA1 :
      A1 =
        4 * S2 +
          9 * S3 +
          16 * S4) :
    4 * S2 / (1 : ℝ) ^ 2 +
        9 * S3 / (1 : ℝ) ^ 3 +
        16 * S4 / (1 : ℝ) ^ 4 =
      A1 := by
  simpa using hA1.symm


/--
The radial Euler differential operator

`D f(r) = r * f'(r)`.

For an inverse-power mode `r⁻ⁿ`, one application gives weight `-n`,
and two applications give weight `n²`.
-/
noncomputable def quznorEulerRadialOperator
    (f : ℝ → ℝ)
    (r : ℝ) : ℝ :=
  r * deriv f r


/--
The inverse-square mode has derivative
`d/dr (S₂ / r²) = -2 S₂ / r³` away from the origin.
-/
theorem quznorInverseSquareMode_hasDerivAt
    (S2 r : ℝ)
    (hr : r ≠ 0) :
    HasDerivAt
      (fun y : ℝ => S2 / y ^ 2)
      (-2 * S2 / r ^ 3)
      r := by
  have hDenominator :
      HasDerivAt
        (fun y : ℝ => y ^ 2)
        (2 * r)
        r := by
    simpa using (hasDerivAt_id r).pow 2

  have hQuotient :=
    (hasDerivAt_const r S2).div
      hDenominator
      (pow_ne_zero 2 hr)

  convert hQuotient using 1 <;>
    field_simp [hr] <;>
    ring


/--
The inverse-cube mode has derivative
`d/dr (S₃ / r³) = -3 S₃ / r⁴` away from the origin.
-/
theorem quznorInverseCubeMode_hasDerivAt
    (S3 r : ℝ)
    (hr : r ≠ 0) :
    HasDerivAt
      (fun y : ℝ => S3 / y ^ 3)
      (-3 * S3 / r ^ 4)
      r := by
  have hDenominator :
      HasDerivAt
        (fun y : ℝ => y ^ 3)
        (3 * r ^ 2)
        r := by
    simpa [id, mul_comm, mul_left_comm, mul_assoc] using
      (hasDerivAt_id r).pow 3

  have hQuotient :=
    (hasDerivAt_const r S3).div
      hDenominator
      (pow_ne_zero 3 hr)

  convert hQuotient using 1 <;>
    field_simp [hr] <;>
    ring


/--
The inverse-fourth mode has derivative
`d/dr (S₄ / r⁴) = -4 S₄ / r⁵` away from the origin.
-/
theorem quznorInverseFourthMode_hasDerivAt
    (S4 r : ℝ)
    (hr : r ≠ 0) :
    HasDerivAt
      (fun y : ℝ => S4 / y ^ 4)
      (-4 * S4 / r ^ 5)
      r := by
  have hDenominator :
      HasDerivAt
        (fun y : ℝ => y ^ 4)
        (4 * r ^ 3)
        r := by
    simpa [id, mul_comm, mul_left_comm, mul_assoc] using
      (hasDerivAt_id r).pow 4

  have hQuotient :=
    (hasDerivAt_const r S4).div
      hDenominator
      (pow_ne_zero 4 hr)

  convert hQuotient using 1 <;>
    field_simp [hr] <;>
    ring


/--
One application of the radial Euler operator to the concrete
three-mode field gives the mode weights `-2`, `-3`, and `-4`.
-/
theorem quznorThreeModeEulerOperator_eq
    (S2 S3 S4 r : ℝ)
    (hr : r ≠ 0) :
    quznorEulerRadialOperator
        (quznorThreeModeAsymptoticField S2 S3 S4)
        r =
      -2 * S2 / r ^ 2 -
        3 * S3 / r ^ 3 -
        4 * S4 / r ^ 4 := by
  have hFieldRaw :=
    ((quznorInverseSquareMode_hasDerivAt S2 r hr).add
      (quznorInverseCubeMode_hasDerivAt S3 r hr)).add
      (quznorInverseFourthMode_hasDerivAt S4 r hr)

  have hField :
      HasDerivAt
        (fun y : ℝ =>
          S2 / y ^ 2 +
            S3 / y ^ 3 +
            S4 / y ^ 4)
        (-(2 * S2) / r ^ 3 +
          -(3 * S3) / r ^ 4 +
          -(4 * S4) / r ^ 5)
        r := by
    convert hFieldRaw using 1 <;>
      try { funext y; rfl } <;>
      ring

  rw [quznorEulerRadialOperator]

  change
    r *
        deriv
          (fun y : ℝ =>
            S2 / y ^ 2 +
              S3 / y ^ 3 +
              S4 / y ^ 4)
          r =
      -2 * S2 / r ^ 2 -
        3 * S3 / r ^ 3 -
        4 * S4 / r ^ 4

  rw [hField.deriv]
  field_simp [hr] <;> ring


/--
The three weighted inverse-power modes have combined derivative
`4*S₂ + 9*S₃ + 16*S₄` at unit radius.
-/
theorem quznorThreeModeEulerModewise_hasDerivAt_one
    (S2 S3 S4 : ℝ) :
    HasDerivAt
      (((fun r : ℝ => (-2 * S2) / r ^ 2) +
          (fun r : ℝ => (-3 * S3) / r ^ 3)) +
        (fun r : ℝ => (-4 * S4) / r ^ 4))
      (4 * S2 + 9 * S3 + 16 * S4)
      1 := by
  have h2 :
      HasDerivAt
        (fun r : ℝ => (-2 * S2) / r ^ 2)
        (4 * S2)
        1 := by
    convert
      quznorInverseSquareMode_hasDerivAt
        (-2 * S2)
        1
        (by norm_num)
      using 1 <;>
        norm_num <;>
        ring_nf

  have h3 :
      HasDerivAt
        (fun r : ℝ => (-3 * S3) / r ^ 3)
        (9 * S3)
        1 := by
    convert
      quznorInverseCubeMode_hasDerivAt
        (-3 * S3)
        1
        (by norm_num)
      using 1 <;>
        norm_num <;>
        ring_nf

  have h4 :
      HasDerivAt
        (fun r : ℝ => (-4 * S4) / r ^ 4)
        (16 * S4)
        1 := by
    convert
      quznorInverseFourthMode_hasDerivAt
        (-4 * S4)
        1
        (by norm_num)
      using 1 <;>
        norm_num <;>
        ring_nf

  exact (h2.add h3).add h4


/--
The actual first Euler-operator field has derivative
`4*S₂ + 9*S₃ + 16*S₄` at unit radius.

The proof transports the verified modewise derivative through the
pointwise Euler identity on the positive neighborhood of `r = 1`.
-/
theorem quznorThreeModeEulerOperator_hasDerivAt_one
    (S2 S3 S4 : ℝ) :
    HasDerivAt
      (fun r : ℝ =>
        quznorEulerRadialOperator
          (quznorThreeModeAsymptoticField S2 S3 S4)
          r)
      (4 * S2 + 9 * S3 + 16 * S4)
      1 := by
  have hModewise :
      HasDerivAt
        (fun r : ℝ =>
          ((-2 * S2) / r ^ 2 +
            (-3 * S3) / r ^ 3) +
            (-4 * S4) / r ^ 4)
        (4 * S2 + 9 * S3 + 16 * S4)
        1 := by
    simpa only [Pi.add_apply] using
      quznorThreeModeEulerModewise_hasDerivAt_one
        S2 S3 S4

  have hEventually :
      (fun r : ℝ =>
        quznorEulerRadialOperator
          (quznorThreeModeAsymptoticField S2 S3 S4)
          r) =ᶠ[nhds (1 : ℝ)]
      (fun r : ℝ =>
        ((-2 * S2) / r ^ 2 +
          (-3 * S3) / r ^ 3) +
          (-4 * S4) / r ^ 4) := by
    filter_upwards [
      Ioi_mem_nhds
        (show (0 : ℝ) < 1 by norm_num)
    ] with r hr

    rw [
      quznorThreeModeEulerOperator_eq
        S2 S3 S4 r (ne_of_gt hr)
    ]
    ring

  exact hModewise.congr_of_eventuallyEq hEventually


/--
Two applications of the radial Euler operator to the concrete
three-mode field give the squared mode weights `2²`, `3²`, and `4²`
at unit radius.
-/
theorem quznorThreeModeSquaredEulerOperator_at_one
    (S2 S3 S4 : ℝ) :
    quznorEulerRadialOperator
        (fun r : ℝ =>
          quznorEulerRadialOperator
            (quznorThreeModeAsymptoticField S2 S3 S4)
            r)
        1 =
      4 * S2 + 9 * S3 + 16 * S4 := by
  change
    (1 : ℝ) *
        deriv
          (fun r : ℝ =>
            quznorEulerRadialOperator
              (quznorThreeModeAsymptoticField S2 S3 S4)
              r)
          1 =
      4 * S2 + 9 * S3 + 16 * S4

  simpa using
    (quznorThreeModeEulerOperator_hasDerivAt_one
      S2 S3 S4).deriv


/--
Under the supplied first asymptotic-coefficient identity, the actual
squared radial Euler operator evaluated at unit radius recovers `A₁`.
-/
theorem quznorThreeModeSquaredEulerOperator_at_one_eq_A1
    (S2 S3 S4 A1 : ℝ)
    (hA1 :
      A1 =
        4 * S2 +
          9 * S3 +
          16 * S4) :
    quznorEulerRadialOperator
        (fun r : ℝ =>
          quznorEulerRadialOperator
            (quznorThreeModeAsymptoticField S2 S3 S4)
            r)
        1 =
      A1 := by
  rw [
    quznorThreeModeSquaredEulerOperator_at_one
      S2 S3 S4
  ]
  exact hA1.symm

end Chronos.Frontier
