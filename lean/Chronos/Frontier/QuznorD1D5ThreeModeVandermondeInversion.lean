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

end Chronos.Frontier
