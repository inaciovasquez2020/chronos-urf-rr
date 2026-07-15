import Mathlib

namespace Chronos
namespace Frontier

noncomputable section

/--
Positive Schwarzschild mass parameter in geometrized units `G = c = 1`.
-/
structure SchwarzschildParameters where
  mass : Real
  mass_pos : 0 < mass

/--
Schwarzschild exterior coordinates represented by `Fin 4 → Real`:

* `0` — time `t`;
* `1` — radius `r`;
* `2` — polar angle `θ`;
* `3` — azimuthal angle `φ`.
-/
def SchwarzschildExteriorDomain (p : SchwarzschildParameters) :=
  {x : Fin 4 → Real //
    2 * p.mass < x 1 ∧
      0 < x 2 ∧
      x 2 < Real.pi}

/-- Schwarzschild lapse factor `1 - 2M/r`. -/
def schwarzschildLapse
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) : Real :=
  1 - 2 * p.mass / x.1 1

/--
Covariant Schwarzschild metric with signature `(-,+,+,+)`:

`diag (-(1 - 2M/r), (1 - 2M/r)⁻¹, r², r² sin² θ)`.
-/
def schwarzschildMetric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    Matrix (Fin 4) (Fin 4) Real :=
  fun μ ν =>
    if μ = 0 ∧ ν = 0 then
      -schwarzschildLapse p x
    else if μ = 1 ∧ ν = 1 then
      (schwarzschildLapse p x)⁻¹
    else if μ = 2 ∧ ν = 2 then
      (x.1 1) ^ 2
    else if μ = 3 ∧ ν = 3 then
      (x.1 1) ^ 2 * Real.sin (x.1 2) ^ 2
    else
      0

/--
Contravariant Schwarzschild metric, defined componentwise as the
diagonal reciprocal of `schwarzschildMetric`.
-/
def schwarzschildInverseMetric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    Matrix (Fin 4) (Fin 4) Real :=
  fun μ ν =>
    if μ = 0 ∧ ν = 0 then
      -((schwarzschildLapse p x)⁻¹)
    else if μ = 1 ∧ ν = 1 then
      schwarzschildLapse p x
    else if μ = 2 ∧ ν = 2 then
      ((x.1 1) ^ 2)⁻¹
    else if μ = 3 ∧ ν = 3 then
      ((x.1 1) ^ 2 * Real.sin (x.1 2) ^ 2)⁻¹
    else
      0

/--
The time-time entry of the covariant metric multiplied by the
contravariant metric is one on the Schwarzschild exterior domain.
-/
theorem schwarzschildMetric_mul_inverse_tt
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (schwarzschildMetric p x * schwarzschildInverseMetric p x) 0 0 =
      1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRatioLtOne :
      2 * p.mass / x.1 1 < 1 := by
    exact (div_lt_one hRadiusPos).2 x.property.1

  have hLapsePos :
      0 < schwarzschildLapse p x := by
    unfold schwarzschildLapse
    linarith

  have hLapseNe :
      schwarzschildLapse p x ≠ 0 :=
    ne_of_gt hLapsePos

  simp [
    Matrix.mul_apply,
    schwarzschildMetric,
    schwarzschildInverseMetric,
    hLapseNe
  ]

/--
The radial-radial entry of the covariant metric multiplied by the
contravariant metric is one on the Schwarzschild exterior domain.
-/
theorem schwarzschildMetric_mul_inverse_rr
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (schwarzschildMetric p x * schwarzschildInverseMetric p x) 1 1 =
      1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRatioLtOne :
      2 * p.mass / x.1 1 < 1 := by
    exact (div_lt_one hRadiusPos).2 x.property.1

  have hLapsePos :
      0 < schwarzschildLapse p x := by
    unfold schwarzschildLapse
    linarith

  have hLapseNe :
      schwarzschildLapse p x ≠ 0 :=
    ne_of_gt hLapsePos

  simp [
    Matrix.mul_apply,
    schwarzschildMetric,
    schwarzschildInverseMetric,
    hLapseNe
  ]

/--
The polar-polar entry of the covariant metric multiplied by the
contravariant metric is one on the Schwarzschild exterior domain.
-/
theorem schwarzschildMetric_mul_inverse_polar
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (schwarzschildMetric p x * schwarzschildInverseMetric p x) 2 2 =
      1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hRadiusSqNe : (x.1 1) ^ 2 ≠ 0 :=
    pow_ne_zero 2 hRadiusNe

  simp [
    Matrix.mul_apply,
    schwarzschildMetric,
    schwarzschildInverseMetric,
    hRadiusSqNe
  ]

/--
The azimuthal-azimuthal entry of the covariant metric multiplied by
the contravariant metric is one on the Schwarzschild exterior domain.
-/
theorem schwarzschildMetric_mul_inverse_azimuthal
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (schwarzschildMetric p x * schwarzschildInverseMetric p x) 3 3 =
      1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusSqNe : (x.1 1) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hRadiusPos)

  have hSinPos : 0 < Real.sin (x.1 2) := by
    exact
      Real.sin_pos_of_pos_of_lt_pi
        x.property.2.1
        x.property.2.2

  have hSinSqNe : Real.sin (x.1 2) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hSinPos)

  simp [
    Matrix.mul_apply,
    schwarzschildMetric,
    schwarzschildInverseMetric
  ]

  field_simp [hRadiusSqNe, hSinSqNe]

/--
Every off-diagonal entry of the Schwarzschild covariant metric
multiplied by its contravariant metric is zero.
-/
theorem schwarzschildMetric_mul_inverse_offDiagonal
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p)
    (μ ν : Fin 4)
    (hμν : μ ≠ ν) :
    (schwarzschildMetric p x * schwarzschildInverseMetric p x) μ ν =
      0 := by
  fin_cases μ <;>
    fin_cases ν <;>
    simp_all [
      Matrix.mul_apply,
      schwarzschildMetric,
      schwarzschildInverseMetric
    ]

/--
The explicitly defined contravariant Schwarzschild metric is a right
matrix inverse of the covariant metric throughout the exterior chart.
-/
theorem schwarzschildMetric_mul_inverse_identity
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    schwarzschildMetric p x * schwarzschildInverseMetric p x =
      (1 : Matrix (Fin 4) (Fin 4) Real) := by
  ext μ ν
  by_cases hμν : μ = ν
  · subst ν
    fin_cases μ
    · simpa using schwarzschildMetric_mul_inverse_tt p x
    · simpa using schwarzschildMetric_mul_inverse_rr p x
    · simpa using schwarzschildMetric_mul_inverse_polar p x
    · simpa using schwarzschildMetric_mul_inverse_azimuthal p x
  · rw [
      schwarzschildMetric_mul_inverse_offDiagonal
        p x μ ν hμν
    ]
    simp [hμν]

/--
The explicitly defined contravariant Schwarzschild metric is also a
left matrix inverse of the covariant metric throughout the exterior chart.
-/
theorem schwarzschildInverseMetric_mul_metric_identity
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    schwarzschildInverseMetric p x * schwarzschildMetric p x =
      (1 : Matrix (Fin 4) (Fin 4) Real) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusSqNe : (x.1 1) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hRadiusPos)

  have hRatioLtOne :
      2 * p.mass / x.1 1 < 1 := by
    exact (div_lt_one hRadiusPos).2 x.property.1

  have hLapsePos :
      0 < schwarzschildLapse p x := by
    unfold schwarzschildLapse
    linarith

  have hLapseNe :
      schwarzschildLapse p x ≠ 0 :=
    ne_of_gt hLapsePos

  have hSinPos : 0 < Real.sin (x.1 2) := by
    exact
      Real.sin_pos_of_pos_of_lt_pi
        x.property.2.1
        x.property.2.2

  have hSinSqNe : Real.sin (x.1 2) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hSinPos)

  ext μ ν
  fin_cases μ <;>
    fin_cases ν <;>
    simp [
      Matrix.mul_apply,
      schwarzschildMetric,
      schwarzschildInverseMetric,
      hLapseNe,
      hRadiusSqNe
    ]

  field_simp [hRadiusSqNe, hSinSqNe]

/--
The radial Schwarzschild time-time metric formula

`g_tt(r) = -(1 - 2M/r)`

has radial derivative `-2M/r²` at every exterior coordinate radius.
-/
theorem schwarzschildMetric_tt_radialFormula_hasDerivAt
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    HasDerivAt
      (fun r : Real => -(1 - 2 * p.mass / r))
      (-(2 * p.mass / (x.1 1) ^ 2))
      (x.1 1) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  (convert
    (((hasDerivAt_const (x.1 1) (1 : Real)).sub
      ((hasDerivAt_const (x.1 1) (2 * p.mass)).fun_div
        (hasDerivAt_id' (x.1 1))
        hRadiusNe)).neg)
    using 1; ring)

/--
The time-time component of the Schwarzschild metric is exactly the
radial formula used by
`schwarzschildMetric_tt_radialFormula_hasDerivAt`.
-/
theorem schwarzschildMetric_tt_eq_radialFormula
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    schwarzschildMetric p x 0 0 =
      -(1 - 2 * p.mass / x.1 1) := by
  simp [
    schwarzschildMetric,
    schwarzschildLapse
  ]

/--
The Schwarzschild Christoffel component obtained from

`Γᵗₜᵣ = (1/2) gᵗᵗ ∂ᵣgₜₜ`

is `M / (r(r - 2M))` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_t_tr_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (1 / 2 : Real) *
        schwarzschildInverseMetric p x 0 0 *
        deriv
          (fun r : Real => -(1 - 2 * p.mass / r))
          (x.1 1) =
      p.mass / (x.1 1 * (x.1 1 - 2 * p.mass)) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hExteriorGapPos :
      0 < x.1 1 - 2 * p.mass := by
    linarith [x.property.1]

  have hExteriorGapNe :
      x.1 1 - 2 * p.mass ≠ 0 :=
    ne_of_gt hExteriorGapPos

  have hDerivative :
      deriv
          (fun r : Real => -(1 - 2 * p.mass / r))
          (x.1 1) =
        -(2 * p.mass / (x.1 1) ^ 2) :=
    (schwarzschildMetric_tt_radialFormula_hasDerivAt p x).deriv

  have hLapseEq :
      schwarzschildLapse p x =
        (x.1 1 - 2 * p.mass) / x.1 1 := by
    unfold schwarzschildLapse
    field_simp [hRadiusNe]

  rw [hDerivative]
  simp [schwarzschildInverseMetric, hLapseEq]
  field_simp [hRadiusNe, hExteriorGapNe]

/--
The Schwarzschild Christoffel component obtained from

`Γʳₜₜ = -(1/2) gʳʳ ∂ᵣgₜₜ`

is `M(r - 2M) / r³` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_tt_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (-(1 / 2 : Real)) *
        schwarzschildInverseMetric p x 1 1 *
        deriv
          (fun r : Real => -(1 - 2 * p.mass / r))
          (x.1 1) =
      p.mass * (x.1 1 - 2 * p.mass) / (x.1 1) ^ 3 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hDerivative :
      deriv
          (fun r : Real => -(1 - 2 * p.mass / r))
          (x.1 1) =
        -(2 * p.mass / (x.1 1) ^ 2) :=
    (schwarzschildMetric_tt_radialFormula_hasDerivAt p x).deriv

  have hLapseEq :
      schwarzschildLapse p x =
        (x.1 1 - 2 * p.mass) / x.1 1 := by
    unfold schwarzschildLapse
    field_simp [hRadiusNe]

  rw [hDerivative]
  simp [schwarzschildInverseMetric, hLapseEq]
  field_simp [hRadiusNe]

/--
The Schwarzschild Christoffel component obtained from

`Γʳᵣᵣ = (1/2) gʳʳ ∂ᵣgᵣᵣ`

with `gᵣᵣ(r) = r / (r - 2M)` is
`-M / (r(r - 2M))` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_rr_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (1 / 2 : Real) *
        schwarzschildInverseMetric p x 1 1 *
        deriv
          (fun r : Real => r / (r - 2 * p.mass))
          (x.1 1) =
      -(p.mass / (x.1 1 * (x.1 1 - 2 * p.mass))) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hExteriorGapPos :
      0 < x.1 1 - 2 * p.mass := by
    linarith [x.property.1]

  have hExteriorGapNe :
      x.1 1 - 2 * p.mass ≠ 0 :=
    ne_of_gt hExteriorGapPos

  have hDerivativeHas :
      HasDerivAt
        (fun r : Real => r / (r - 2 * p.mass))
        (-(2 * p.mass) / (x.1 1 - 2 * p.mass) ^ 2)
        (x.1 1) := by
    (convert
      (hasDerivAt_id' (x.1 1)).fun_div
        ((hasDerivAt_id' (x.1 1)).sub
          (hasDerivAt_const (x.1 1) (2 * p.mass)))
        hExteriorGapNe
      using 1;
        simp only [Pi.sub_apply];
        field_simp [hExteriorGapNe];
        ring)

  have hDerivative :
      deriv
          (fun r : Real => r / (r - 2 * p.mass))
          (x.1 1) =
        -(2 * p.mass) / (x.1 1 - 2 * p.mass) ^ 2 :=
    hDerivativeHas.deriv

  have hLapseEq :
      schwarzschildLapse p x =
        (x.1 1 - 2 * p.mass) / x.1 1 := by
    unfold schwarzschildLapse
    field_simp [hRadiusNe]

  rw [hDerivative]
  simp [schwarzschildInverseMetric, hLapseEq]
  field_simp [hRadiusNe, hExteriorGapNe]

/--
The Schwarzschild Christoffel component obtained from

`Γʳ_θθ = -(1/2) gʳʳ ∂ᵣg_θθ`

with `g_θθ(r) = r²` is `-(r - 2M)` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_theta_theta_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (-(1 / 2 : Real)) *
        schwarzschildInverseMetric p x 1 1 *
        deriv
          (fun r : Real => r ^ 2)
          (x.1 1) =
      -(x.1 1 - 2 * p.mass) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hDerivativeHas :
      HasDerivAt
        (fun r : Real => r ^ 2)
        (2 * x.1 1)
        (x.1 1) := by
    simpa [pow_two, two_mul] using
      ((hasDerivAt_id' (x.1 1)).mul
        (hasDerivAt_id' (x.1 1)))

  have hDerivative :
      deriv
          (fun r : Real => r ^ 2)
          (x.1 1) =
        2 * x.1 1 :=
    hDerivativeHas.deriv

  have hInverseRR :
      schwarzschildInverseMetric p x 1 1 =
        schwarzschildLapse p x := by
    simp [schwarzschildInverseMetric]

  have hLapseEq :
      schwarzschildLapse p x =
        (x.1 1 - 2 * p.mass) / x.1 1 := by
    unfold schwarzschildLapse
    field_simp [hRadiusNe]

  rw [hDerivative, hInverseRR, hLapseEq]
  field_simp [hRadiusNe]

/--
The Schwarzschild Christoffel component obtained from

`Γʳ_φφ = -(1/2) gʳʳ ∂ᵣg_φφ`

with `g_φφ(r, θ) = r² sin² θ` is
`-(r - 2M) sin² θ` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_phi_phi_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (-(1 / 2 : Real)) *
        schwarzschildInverseMetric p x 1 1 *
        deriv
          (fun r : Real =>
            r ^ 2 * Real.sin (x.1 2) ^ 2)
          (x.1 1) =
      -(x.1 1 - 2 * p.mass) *
        Real.sin (x.1 2) ^ 2 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hSquareDerivative :
      HasDerivAt
        (fun r : Real => r ^ 2)
        (2 * x.1 1)
        (x.1 1) := by
    simpa [pow_two, two_mul] using
      ((hasDerivAt_id' (x.1 1)).mul
        (hasDerivAt_id' (x.1 1)))

  have hDerivativeHas :
      HasDerivAt
        (fun r : Real =>
          r ^ 2 * Real.sin (x.1 2) ^ 2)
        ((2 * x.1 1) * Real.sin (x.1 2) ^ 2)
        (x.1 1) := by
    simpa using
      hSquareDerivative.mul
        (hasDerivAt_const
          (x.1 1)
          (Real.sin (x.1 2) ^ 2))

  have hDerivative :
      deriv
          (fun r : Real =>
            r ^ 2 * Real.sin (x.1 2) ^ 2)
          (x.1 1) =
        (2 * x.1 1) * Real.sin (x.1 2) ^ 2 :=
    hDerivativeHas.deriv

  have hInverseRR :
      schwarzschildInverseMetric p x 1 1 =
        schwarzschildLapse p x := by
    simp [schwarzschildInverseMetric]

  have hLapseEq :
      schwarzschildLapse p x =
        (x.1 1 - 2 * p.mass) / x.1 1 := by
    unfold schwarzschildLapse
    field_simp [hRadiusNe]

  rw [hDerivative, hInverseRR, hLapseEq]
  field_simp [hRadiusNe]

/--
The Schwarzschild Christoffel component obtained from

`Γθ_rθ = (1/2) gθθ ∂ᵣg_θθ`

with `g_θθ(r) = r²` is `1/r` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_theta_r_theta_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (1 / 2 : Real) *
        schwarzschildInverseMetric p x 2 2 *
        deriv
          (fun r : Real => r ^ 2)
          (x.1 1) =
      1 / x.1 1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hDerivativeHas :
      HasDerivAt
        (fun r : Real => r ^ 2)
        (2 * x.1 1)
        (x.1 1) := by
    simpa [pow_two, two_mul] using
      ((hasDerivAt_id' (x.1 1)).mul
        (hasDerivAt_id' (x.1 1)))

  have hDerivative :
      deriv
          (fun r : Real => r ^ 2)
          (x.1 1) =
        2 * x.1 1 :=
    hDerivativeHas.deriv

  have hAlgebra :
      (1 / 2 : Real) *
          ((x.1 1) ^ 2)⁻¹ *
          (2 * x.1 1) =
        1 / x.1 1 := by
    field_simp [hRadiusNe]

  rw [hDerivative]
  simpa [schwarzschildInverseMetric] using hAlgebra

/--
The Schwarzschild Christoffel component obtained from

`Γφ_rφ = (1/2) gφφ ∂ᵣg_φφ`

with `g_φφ(r, θ) = r² sin² θ` is `1/r` throughout the
exterior chart.
-/
theorem schwarzschildChristoffel_phi_r_phi_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (1 / 2 : Real) *
        schwarzschildInverseMetric p x 3 3 *
        deriv
          (fun r : Real =>
            r ^ 2 * Real.sin (x.1 2) ^ 2)
          (x.1 1) =
      1 / x.1 1 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hSinPos : 0 < Real.sin (x.1 2) := by
    exact
      Real.sin_pos_of_pos_of_lt_pi
        x.property.2.1
        x.property.2.2

  have hSinSqNe : Real.sin (x.1 2) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hSinPos)

  have hSquareDerivative :
      HasDerivAt
        (fun r : Real => r ^ 2)
        (2 * x.1 1)
        (x.1 1) := by
    simpa [pow_two, two_mul] using
      ((hasDerivAt_id' (x.1 1)).mul
        (hasDerivAt_id' (x.1 1)))

  have hDerivativeHas :
      HasDerivAt
        (fun r : Real =>
          r ^ 2 * Real.sin (x.1 2) ^ 2)
        ((2 * x.1 1) * Real.sin (x.1 2) ^ 2)
        (x.1 1) := by
    simpa using
      hSquareDerivative.mul
        (hasDerivAt_const
          (x.1 1)
          (Real.sin (x.1 2) ^ 2))

  have hDerivative :
      deriv
          (fun r : Real =>
            r ^ 2 * Real.sin (x.1 2) ^ 2)
          (x.1 1) =
        (2 * x.1 1) * Real.sin (x.1 2) ^ 2 :=
    hDerivativeHas.deriv

  have hAlgebra :
      (1 / 2 : Real) *
          ((x.1 1) ^ 2 *
            Real.sin (x.1 2) ^ 2)⁻¹ *
          ((2 * x.1 1) *
            Real.sin (x.1 2) ^ 2) =
        1 / x.1 1 := by
    field_simp [hRadiusNe, hSinSqNe]

  rw [hDerivative]
  simpa [schwarzschildInverseMetric] using hAlgebra

/--
The Schwarzschild Christoffel component obtained from

`Γθ_φφ = -(1/2) gθθ ∂θg_φφ`

with `g_φφ(r, θ) = r² sin² θ` is
`-sin θ cos θ` throughout the exterior chart.
-/
theorem schwarzschildChristoffel_theta_phi_phi_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (-(1 / 2 : Real)) *
        schwarzschildInverseMetric p x 2 2 *
        deriv
          (fun θ : Real =>
            (x.1 1) ^ 2 * Real.sin θ ^ 2)
          (x.1 2) =
      -(Real.sin (x.1 2) * Real.cos (x.1 2)) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusSqNe : (x.1 1) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hRadiusPos)

  have hSinSquareDerivative :
      HasDerivAt
        (fun θ : Real => Real.sin θ ^ 2)
        (Real.cos (x.1 2) * Real.sin (x.1 2) +
          Real.sin (x.1 2) * Real.cos (x.1 2))
        (x.1 2) := by
    simpa [pow_two] using
      (Real.hasDerivAt_sin (x.1 2)).mul
        (Real.hasDerivAt_sin (x.1 2))

  have hDerivativeHas :
      HasDerivAt
        (fun θ : Real =>
          (x.1 1) ^ 2 * Real.sin θ ^ 2)
        ((x.1 1) ^ 2 *
          (Real.cos (x.1 2) * Real.sin (x.1 2) +
            Real.sin (x.1 2) * Real.cos (x.1 2)))
        (x.1 2) := by
    simpa using
      (hasDerivAt_const (x.1 2) ((x.1 1) ^ 2)).mul
        hSinSquareDerivative

  have hDerivative :
      deriv
          (fun θ : Real =>
            (x.1 1) ^ 2 * Real.sin θ ^ 2)
          (x.1 2) =
        (x.1 1) ^ 2 *
          (Real.cos (x.1 2) * Real.sin (x.1 2) +
            Real.sin (x.1 2) * Real.cos (x.1 2)) :=
    hDerivativeHas.deriv

  have hAlgebra :
      (-(1 / 2 : Real)) *
          ((x.1 1) ^ 2)⁻¹ *
          ((x.1 1) ^ 2 *
            (Real.cos (x.1 2) * Real.sin (x.1 2) +
              Real.sin (x.1 2) * Real.cos (x.1 2))) =
        -(Real.sin (x.1 2) * Real.cos (x.1 2)) := by
    (field_simp [hRadiusSqNe]; ring)

  rw [hDerivative]
  simpa [schwarzschildInverseMetric] using hAlgebra


/--
The Schwarzschild Christoffel component obtained from
`Γφ_θφ = (1/2) gφφ ∂θg_φφ` with
`g_φφ(r, θ) = r² sin² θ` is `cos θ / sin θ` throughout
the exterior chart.
-/
theorem schwarzschildChristoffel_phi_theta_phi_from_metric
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (1 / 2 : Real) *
        schwarzschildInverseMetric p x 3 3 *
        deriv
          (fun θ : Real =>
            (x.1 1) ^ 2 * Real.sin θ ^ 2)
          (x.1 2) =
      Real.cos (x.1 2) / Real.sin (x.1 2) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusSqNe : (x.1 1) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 (ne_of_gt hRadiusPos)

  have hSinPos : 0 < Real.sin (x.1 2) := by
    exact
      Real.sin_pos_of_pos_of_lt_pi
        x.property.2.1
        x.property.2.2

  have hSinNe : Real.sin (x.1 2) ≠ 0 := by
    exact ne_of_gt hSinPos

  have hSinSqNe : Real.sin (x.1 2) ^ 2 ≠ 0 := by
    exact pow_ne_zero 2 hSinNe

  have hSinSquareDerivative :
      HasDerivAt
        (fun θ : Real => Real.sin θ ^ 2)
        (Real.cos (x.1 2) * Real.sin (x.1 2) +
          Real.sin (x.1 2) * Real.cos (x.1 2))
        (x.1 2) := by
    simpa [pow_two] using
      (Real.hasDerivAt_sin (x.1 2)).mul
        (Real.hasDerivAt_sin (x.1 2))

  have hDerivativeHas :
      HasDerivAt
        (fun θ : Real =>
          (x.1 1) ^ 2 * Real.sin θ ^ 2)
        ((x.1 1) ^ 2 *
          (Real.cos (x.1 2) * Real.sin (x.1 2) +
            Real.sin (x.1 2) * Real.cos (x.1 2)))
        (x.1 2) := by
    simpa using
      (hasDerivAt_const
        (x.1 2)
        ((x.1 1) ^ 2)).mul hSinSquareDerivative

  have hDerivative :
      deriv
          (fun θ : Real =>
            (x.1 1) ^ 2 * Real.sin θ ^ 2)
          (x.1 2) =
        (x.1 1) ^ 2 *
          (Real.cos (x.1 2) * Real.sin (x.1 2) +
            Real.sin (x.1 2) * Real.cos (x.1 2)) :=
    hDerivativeHas.deriv

  have hAlgebra :
      (1 / 2 : Real) *
          ((x.1 1) ^ 2 * Real.sin (x.1 2) ^ 2)⁻¹ *
          ((x.1 1) ^ 2 *
            (Real.cos (x.1 2) * Real.sin (x.1 2) +
              Real.sin (x.1 2) * Real.cos (x.1 2))) =
        Real.cos (x.1 2) / Real.sin (x.1 2) := by
    (field_simp [hRadiusSqNe, hSinNe, hSinSqNe]; ring)

  rw [hDerivative]
  simpa [schwarzschildInverseMetric] using hAlgebra


/--
The thirteen ordered nonzero Levi-Civita connection coefficients of the
Schwarzschild metric in the coordinate order

`0 = t`, `1 = r`, `2 = θ`, `3 = φ`.

The lower-index symmetric partners are listed explicitly. Every other
ordered coefficient is zero.
-/
def schwarzschildChristoffel
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p)
    (ρ μ ν : Fin 4) : Real :=
  if ρ = 0 ∧ μ = 0 ∧ ν = 1 then
    p.mass /
      (x.1 1 * (x.1 1 - 2 * p.mass))
  else if ρ = 0 ∧ μ = 1 ∧ ν = 0 then
    p.mass /
      (x.1 1 * (x.1 1 - 2 * p.mass))
  else if ρ = 1 ∧ μ = 0 ∧ ν = 0 then
    p.mass * (x.1 1 - 2 * p.mass) /
      (x.1 1) ^ 3
  else if ρ = 1 ∧ μ = 1 ∧ ν = 1 then
    -(p.mass /
      (x.1 1 * (x.1 1 - 2 * p.mass)))
  else if ρ = 1 ∧ μ = 2 ∧ ν = 2 then
    -(x.1 1 - 2 * p.mass)
  else if ρ = 1 ∧ μ = 3 ∧ ν = 3 then
    -(x.1 1 - 2 * p.mass) *
      Real.sin (x.1 2) ^ 2
  else if ρ = 2 ∧ μ = 1 ∧ ν = 2 then
    (1 : Real) / x.1 1
  else if ρ = 2 ∧ μ = 2 ∧ ν = 1 then
    (1 : Real) / x.1 1
  else if ρ = 3 ∧ μ = 1 ∧ ν = 3 then
    (1 : Real) / x.1 1
  else if ρ = 3 ∧ μ = 3 ∧ ν = 1 then
    (1 : Real) / x.1 1
  else if ρ = 2 ∧ μ = 3 ∧ ν = 3 then
    -(Real.sin (x.1 2) * Real.cos (x.1 2))
  else if ρ = 3 ∧ μ = 2 ∧ ν = 3 then
    Real.cos (x.1 2) / Real.sin (x.1 2)
  else if ρ = 3 ∧ μ = 3 ∧ ν = 2 then
    Real.cos (x.1 2) / Real.sin (x.1 2)
  else
    0


/--
The contracted Schwarzschild connection coefficient in the radial
coordinate is

`∑ α, Γ^α_{rα} = 2 / r`.

The time-radial and radial-radial terms cancel, leaving the polar and
azimuthal contributions `1 / r + 1 / r`.
-/
theorem schwarzschildChristoffel_radialTrace
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (∑ α : Fin 4,
      schwarzschildChristoffel p x α 1 α) =
        2 / x.1 1 := by
  (simp [
    Fin.sum_univ_four,
    schwarzschildChristoffel,
    div_eq_mul_inv
  ]; ring)


/--
The contracted Schwarzschild connection coefficient in the polar
coordinate is

`∑ α, Γ^α_{θα} = cos θ / sin θ`.

The only nonzero summand is `Γ^φ_{θφ}`.
-/
theorem schwarzschildChristoffel_polarTrace
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (∑ α : Fin 4,
      schwarzschildChristoffel p x α 2 α) =
        Real.cos (x.1 2) / Real.sin (x.1 2) := by
  simp [
    Fin.sum_univ_four,
    schwarzschildChristoffel
  ]


/--
The contracted Schwarzschild connection coefficient in the temporal
coordinate vanishes:

`∑ α, Γ^α_{tα} = 0`.

Every summand is outside the thirteen-entry nonzero support table.
-/
theorem schwarzschildChristoffel_temporalTrace
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (∑ α : Fin 4,
      schwarzschildChristoffel p x α 0 α) =
        0 := by
  simp [
    Fin.sum_univ_four,
    schwarzschildChristoffel
  ]


/--
The contracted Schwarzschild connection coefficient in the azimuthal
coordinate vanishes:

`∑ α, Γ^α_{φα} = 0`.

Every summand is outside the thirteen-entry nonzero support table.
-/
theorem schwarzschildChristoffel_azimuthalTrace
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    (∑ α : Fin 4,
      schwarzschildChristoffel p x α 3 α) =
        0 := by
  simp [
    Fin.sum_univ_four,
    schwarzschildChristoffel
  ]


/--
The radial derivative of the packaged Schwarzschild coefficient

`Γʳₜₜ(r) = M(r - 2M) / r³`

is

`-2M(r - 3M) / r⁴`

throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_tt_radialFormula_hasDerivAt
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    HasDerivAt
      (fun r : Real =>
        p.mass * (r - 2 * p.mass) / r ^ 3)
      (-(2 * p.mass * (x.1 1 - 3 * p.mass) /
        (x.1 1) ^ 4))
      (x.1 1) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hRadiusCubeNe : (x.1 1) ^ 3 ≠ 0 :=
    pow_ne_zero 3 hRadiusNe

  have hNumerator :
      HasDerivAt
        (fun r : Real =>
          p.mass * (r - 2 * p.mass))
        p.mass
        (x.1 1) := by
    simpa using
      (hasDerivAt_const (x.1 1) p.mass).mul
        ((hasDerivAt_id' (x.1 1)).sub
          (hasDerivAt_const
            (x.1 1)
            (2 * p.mass)))

  have hDenominator :
      HasDerivAt
        (fun r : Real => r ^ 3)
        (3 * (x.1 1) ^ 2)
        (x.1 1) := by
    simpa using
      (hasDerivAt_id' (x.1 1)).pow 3

  have hDerivative :
      HasDerivAt
        (fun r : Real =>
          p.mass * (r - 2 * p.mass) / r ^ 3)
        ((p.mass * (x.1 1) ^ 3 -
            (p.mass * (x.1 1 - 2 * p.mass)) *
              (3 * (x.1 1) ^ 2)) /
          ((x.1 1) ^ 3) ^ 2)
        (x.1 1) :=
    hNumerator.fun_div
      hDenominator
      hRadiusCubeNe

  have hAlgebra :
      ((p.mass * (x.1 1) ^ 3 -
            (p.mass * (x.1 1 - 2 * p.mass)) *
              (3 * (x.1 1) ^ 2)) /
          ((x.1 1) ^ 3) ^ 2) =
        -(2 * p.mass * (x.1 1 - 3 * p.mass) /
          (x.1 1) ^ 4) := by
    field_simp [hRadiusNe]
    ring

  rw [hAlgebra] at hDerivative
  exact hDerivative


/--
The nonzero terms in the Schwarzschild `tt` Ricci-component formula
cancel exactly:

`∂ᵣ Γʳₜₜ + Γʳₜₜ (∑ α, Γ^α_{rα})
  - Γᵗₜᵣ Γʳₜₜ - Γʳₜₜ Γᵗₜᵣ = 0`.

The omitted temporal-trace derivative is zero because the temporal
contracted connection coefficient vanishes.
-/
theorem schwarzschildRicci_tt_reducedExpression_eq_zero
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    deriv
        (fun r : Real =>
          p.mass * (r - 2 * p.mass) / r ^ 3)
        (x.1 1) +
      schwarzschildChristoffel p x 1 0 0 *
        (∑ α : Fin 4,
          schwarzschildChristoffel p x α 1 α) -
      (schwarzschildChristoffel p x 0 0 1 *
          schwarzschildChristoffel p x 1 0 0 +
        schwarzschildChristoffel p x 1 0 0 *
          schwarzschildChristoffel p x 0 0 1) =
      0 := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hExteriorGapPos :
      0 < x.1 1 - 2 * p.mass := by
    linarith [x.property.1]

  have hExteriorGapNe :
      x.1 1 - 2 * p.mass ≠ 0 :=
    ne_of_gt hExteriorGapPos

  rw [
    (schwarzschildChristoffel_r_tt_radialFormula_hasDerivAt
      p
      x).deriv,
    schwarzschildChristoffel_radialTrace p x
  ]

  simp [schwarzschildChristoffel]

  (field_simp [hRadiusNe, hExteriorGapNe]; ring)


/--
The coordinate partial derivative of a scalar field on the raw
Schwarzschild coordinate array.

`schwarzschildCoordinatePartial coord f x` varies only coordinate
`coord` through `Function.update`, holds the other three coordinates
fixed, and applies Mathlib's one-variable derivative at `x coord`.
-/
def schwarzschildCoordinatePartial
    (coord : Fin 4)
    (f : (Fin 4 → Real) → Real)
    (x : Fin 4 → Real) : Real :=
  deriv
    (fun value : Real =>
      f (Function.update x coord value))
    (x coord)


/--
The Schwarzschild connection-coefficient field on an unrestricted raw
coordinate array.

This has the same thirteen-entry support and coordinate formulas as
`schwarzschildChristoffel`, but does not require an exterior-domain
subtype. It can therefore be varied by `schwarzschildCoordinatePartial`.
-/
def schwarzschildChristoffelRaw
    (mass : Real)
    (x : Fin 4 → Real)
    (ρ μ ν : Fin 4) : Real :=
  if ρ = 0 ∧ μ = 0 ∧ ν = 1 then
    mass / (x 1 * (x 1 - 2 * mass))
  else if ρ = 0 ∧ μ = 1 ∧ ν = 0 then
    mass / (x 1 * (x 1 - 2 * mass))
  else if ρ = 1 ∧ μ = 0 ∧ ν = 0 then
    mass * (x 1 - 2 * mass) / (x 1) ^ 3
  else if ρ = 1 ∧ μ = 1 ∧ ν = 1 then
    -(mass / (x 1 * (x 1 - 2 * mass)))
  else if ρ = 1 ∧ μ = 2 ∧ ν = 2 then
    -(x 1 - 2 * mass)
  else if ρ = 1 ∧ μ = 3 ∧ ν = 3 then
    -(x 1 - 2 * mass) * Real.sin (x 2) ^ 2
  else if ρ = 2 ∧ μ = 1 ∧ ν = 2 then
    (1 : Real) / x 1
  else if ρ = 2 ∧ μ = 2 ∧ ν = 1 then
    (1 : Real) / x 1
  else if ρ = 3 ∧ μ = 1 ∧ ν = 3 then
    (1 : Real) / x 1
  else if ρ = 3 ∧ μ = 3 ∧ ν = 1 then
    (1 : Real) / x 1
  else if ρ = 2 ∧ μ = 3 ∧ ν = 3 then
    -(Real.sin (x 2) * Real.cos (x 2))
  else if ρ = 3 ∧ μ = 2 ∧ ν = 3 then
    Real.cos (x 2) / Real.sin (x 2)
  else if ρ = 3 ∧ μ = 3 ∧ ν = 2 then
    Real.cos (x 2) / Real.sin (x 2)
  else
    0


/--
The unrestricted raw-coordinate Schwarzschild connection field agrees
definitionally with the exterior-domain connection table at every valid
exterior point.
-/
theorem schwarzschildChristoffelRaw_eq_exterior
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p)
    (ρ μ ν : Fin 4) :
    schwarzschildChristoffelRaw
        p.mass
        x.1
        ρ
        μ
        ν =
      schwarzschildChristoffel
        p
        x
        ρ
        μ
        ν := by
  rfl


/--
The coordinate Ricci tensor constructed from the unrestricted
Schwarzschild connection field using the convention

`R_μν =
  ∂_λ Γ^λ_μν
  - ∂_ν Γ^λ_μλ
  + Γ^λ_μν Γ^σ_λσ
  - Γ^σ_μλ Γ^λ_νσ`.
-/
def schwarzschildRicciRaw
    (mass : Real)
    (x : Fin 4 → Real)
    (μ ν : Fin 4) : Real :=
  (∑ coord : Fin 4,
    schwarzschildCoordinatePartial
      coord
      (fun y : Fin 4 → Real =>
        schwarzschildChristoffelRaw
          mass
          y
          coord
          μ
          ν)
      x) -
  (∑ coord : Fin 4,
    schwarzschildCoordinatePartial
      ν
      (fun y : Fin 4 → Real =>
        schwarzschildChristoffelRaw
          mass
          y
          coord
          μ
          coord)
      x) +
  (∑ coord : Fin 4,
    ∑ sigma : Fin 4,
      schwarzschildChristoffelRaw
          mass
          x
          coord
          μ
          ν *
        schwarzschildChristoffelRaw
          mass
          x
          sigma
          coord
          sigma) -
  (∑ coord : Fin 4,
    ∑ sigma : Fin 4,
      schwarzschildChristoffelRaw
          mass
          x
          sigma
          μ
          coord *
        schwarzschildChristoffelRaw
          mass
          x
          coord
          ν
          sigma)


/--
The complete coordinate time-time component of the Schwarzschild Ricci
tensor vanishes throughout the exterior chart.
-/
theorem schwarzschildRicciRaw_tt_eq_zero
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    schwarzschildRicciRaw
        p.mass
        x.1
        0
        0 =
      0 := by
  have hReduced :=
    schwarzschildRicci_tt_reducedExpression_eq_zero p x

  simp [
    schwarzschildRicciRaw,
    schwarzschildCoordinatePartial,
    schwarzschildChristoffelRaw,
    schwarzschildChristoffel,
    Fin.sum_univ_four
  ] at hReduced ⊢

  ring_nf at hReduced ⊢
  exact hReduced


/--
The radial derivative of the Schwarzschild coefficient

`Γʳᵣᵣ(r) = -M / (r(r - 2M))`

is

`2M(r - M) / (r²(r - 2M)²)`

throughout the exterior chart.
-/
theorem schwarzschildChristoffel_r_rr_radialFormula_hasDerivAt
    (p : SchwarzschildParameters)
    (x : SchwarzschildExteriorDomain p) :
    HasDerivAt
      (fun r : Real =>
        -(p.mass / (r * (r - 2 * p.mass))))
      (2 * p.mass * (x.1 1 - p.mass) /
        ((x.1 1) ^ 2 *
          (x.1 1 - 2 * p.mass) ^ 2))
      (x.1 1) := by
  have hRadiusPos : 0 < x.1 1 := by
    nlinarith [p.mass_pos, x.property.1]

  have hRadiusNe : x.1 1 ≠ 0 :=
    ne_of_gt hRadiusPos

  have hExteriorGapPos :
      0 < x.1 1 - 2 * p.mass := by
    linarith [x.property.1]

  have hExteriorGapNe :
      x.1 1 - 2 * p.mass ≠ 0 :=
    ne_of_gt hExteriorGapPos

  have hDenominatorNe :
      x.1 1 * (x.1 1 - 2 * p.mass) ≠ 0 :=
    mul_ne_zero hRadiusNe hExteriorGapNe

  have hDenominator :
      HasDerivAt
        (fun r : Real =>
          r * (r - 2 * p.mass))
        (2 * (x.1 1 - p.mass))
        (x.1 1) := by
    convert
      (hasDerivAt_id' (x.1 1)).mul
        ((hasDerivAt_id' (x.1 1)).sub
          (hasDerivAt_const
            (x.1 1)
            (2 * p.mass))) using 1
    all_goals
      simp only [Pi.sub_apply]
      ring

  convert
    ((hasDerivAt_const
        (x.1 1)
        p.mass).fun_div
      hDenominator
      hDenominatorNe).neg using 1
  all_goals
    field_simp [hRadiusNe, hExteriorGapNe]
    ring

/--
Exact differential identity underlying radial Einstein-defect
reconstruction: if `F₀` has zero defect and `F` has defect `E`, then
the derivative of `x * (F - F₀)` is exactly `E`.
-/
theorem schwarzschildRadialDefect_hasDerivAt_mul_sub
    (F F₀ : ℝ → ℝ)
    (x F' F₀' E : ℝ)
    (hF : HasDerivAt F F' x)
    (hF₀ : HasDerivAt F₀ F₀' x)
    (hBaseline : x * F₀' + F₀ x - 1 = 0)
    (hDefect : E = x * F' + F x - 1) :
    HasDerivAt
      (fun y => y * (F y - F₀ y))
      E
      x := by
  have hProduct :
      HasDerivAt
        (fun y => y * (F y - F₀ y))
        ((F x - F₀ x) + x * (F' - F₀'))
        x := by
    simpa using (hasDerivAt_id x).mul (hF.sub hF₀)

  have hCoefficient :
      (F x - F₀ x) + x * (F' - F₀') = E := by
    calc
      (F x - F₀ x) + x * (F' - F₀') =
          x * F' + F x - (x * F₀' + F₀ x) := by
            ring
      _ = E := by
        linarith

  rw [hCoefficient] at hProduct
  exact hProduct

/--
Scalar photon equation for a reconstructed radial defect.

The reconstruction relation is the denominator-free form

`x * F = x - 2 - I_e`,

the defect equation is

`e = x * F' + F - 1`,

and the photon-sphere equation is

`x * F' - 2 * F = 0`.

Together they imply

`2 * (3 - x) + x * e + 3 * I_e = 0`.
-/
theorem schwarzschildScalarPhotonEquation_of_reconstruction
    (x e I_e F F' : ℝ)
    (hReconstruction : x * F = x - 2 - I_e)
    (hDefect : e = x * F' + F - 1)
    (hPhoton : x * F' - 2 * F = 0) :
    2 * (3 - x) + x * e + 3 * I_e = 0 := by
  have he : e = 3 * F - 1 := by
    linarith

  have hxe : x * e = 3 * (x * F) - x := by
    rw [he]
    ring

  rw [hReconstruction] at hxe
  linarith

/--
The algebraic estimate used in the quadratic photon-root remainder.

Writing the remainder as

`(x - 3) * e(x) + 3 * (e(x) - e(3)) - 3 * integralDelta`,

the pointwise defect bound, Lipschitz defect bound, and integral bound
give the explicit coefficient seven.
-/
theorem schwarzschildPhotonRootRemainder_abs_le_seven
    (x eAtX eAtThree integralDelta δ R : ℝ)
    (heAtX :
      |eAtX| ≤ δ)
    (heVariation :
      |eAtX - eAtThree| ≤ δ * |x - 3|)
    (hIntegral :
      |integralDelta| ≤ δ * |x - 3|)
    (hR :
      R =
        x * eAtX -
          3 * eAtThree -
          3 * integralDelta) :
    |R| ≤ 7 * δ * |x - 3| := by
  have hRDecomposition :
      R =
        (x - 3) * eAtX +
          3 * (eAtX - eAtThree) -
          3 * integralDelta := by
    rw [hR]
    ring

  have hAtX :
      |(x - 3) * eAtX| ≤
        δ * |x - 3| := by
    calc
      |(x - 3) * eAtX| =
          |x - 3| * |eAtX| := by
            rw [abs_mul]
      _ ≤ |x - 3| * δ :=
        mul_le_mul_of_nonneg_left
          heAtX
          (abs_nonneg (x - 3))
      _ = δ * |x - 3| := by
        ring

  have hVariationTerm :
      |3 * (eAtX - eAtThree)| ≤
        3 * (δ * |x - 3|) := by
    calc
      |3 * (eAtX - eAtThree)| =
          3 * |eAtX - eAtThree| := by
            rw [abs_mul]
            norm_num
      _ ≤ 3 * (δ * |x - 3|) :=
        mul_le_mul_of_nonneg_left
          heVariation
          (by norm_num)

  have hIntegralTerm :
      |3 * integralDelta| ≤
        3 * (δ * |x - 3|) := by
    calc
      |3 * integralDelta| =
          3 * |integralDelta| := by
            rw [abs_mul]
            norm_num
      _ ≤ 3 * (δ * |x - 3|) :=
        mul_le_mul_of_nonneg_left
          hIntegral
          (by norm_num)

  rw [hRDecomposition]

  calc
    |(x - 3) * eAtX +
        3 * (eAtX - eAtThree) -
        3 * integralDelta| ≤
        |(x - 3) * eAtX +
          3 * (eAtX - eAtThree)| +
        |3 * integralDelta| := by
          exact
            abs_sub
              ((x - 3) * eAtX +
                3 * (eAtX - eAtThree))
              (3 * integralDelta)
    _ ≤
        (|(x - 3) * eAtX| +
          |3 * (eAtX - eAtThree)|) +
        |3 * integralDelta| := by
          exact
            add_le_add
              (by
                simpa [sub_eq_add_neg, abs_neg] using
                  (abs_sub
                    ((x - 3) * eAtX)
                    (-(3 * (eAtX - eAtThree)))))
              (le_refl |3 * integralDelta|)
    _ ≤
        (δ * |x - 3| +
          3 * (δ * |x - 3|)) +
        3 * (δ * |x - 3|) := by
          exact
            add_le_add
              (add_le_add hAtX hVariationTerm)
              hIntegralTerm
    _ = 7 * δ * |x - 3| := by
          ring

/--
Closed-form photon-sphere root for the constant negative defect
`e = -t`, whose reconstructed integral is `I_e(x) = -t * (b - x)`.

The scalar photon equation becomes

`2 * (3 - x) - x * t - 3 * t * (b - x) = 0`,

and therefore, provided `t ≠ 1`,

`x = 3 * (2 - b * t) / (2 * (1 - t))`.
-/
theorem schwarzschildConstantNegativeDefect_photonRoot_closedForm
    (b t x : ℝ)
    (ht : 1 - t ≠ 0)
    (hPhoton :
      2 * (3 - x) -
          x * t -
          3 * t * (b - x) =
        0) :
    x =
      3 * (2 - b * t) /
        (2 * (1 - t)) := by
  have hLinear :
      2 * (1 - t) * x =
        3 * (2 - b * t) := by
    linarith

  have hDenominator :
      2 * (1 - t) ≠ 0 := by
    exact
      mul_ne_zero
        (by norm_num)
        ht

  apply (eq_div_iff hDenominator).2
  simpa [mul_assoc, mul_comm, mul_left_comm] using hLinear

/--
Exact shadow formula for the constant negative-defect photon root.

If

`x = 3 * (2 - b * t) / (2 * (1 - t))`

and the reconstructed metric coefficient at that root is

`F(x) = (1 - t) / 3`,

then the shadow impact parameter `B = x / sqrt(F(x))` has the
corresponding closed form.
-/
theorem schwarzschildConstantNegativeDefect_shadow_closedForm
    (b t x FAtRoot B : ℝ)
    (hRoot :
      x =
        3 * (2 - b * t) /
          (2 * (1 - t)))
    (hMetricAtRoot :
      FAtRoot = (1 - t) / 3)
    (hShadow :
      B = x / Real.sqrt FAtRoot) :
    B =
      (3 * (2 - b * t) /
          (2 * (1 - t))) /
        Real.sqrt ((1 - t) / 3) := by
  rw [hShadow, hRoot, hMetricAtRoot]


/--
For a constant negative defect, the exact nonlinear quantity `K₋(t)`
strictly exceeds its first-order comparison value `K_lin`.

The hypotheses `3 < b`, `0 < t < 1`, and `b * t < 2` keep the
constant-defect photon root in the positive exterior branch.
-/
theorem schwarzschildConstantNegativeDefect_Kminus_gt_Klin
    (b t : ℝ)
    (hb : 3 < b)
    (ht : 0 < t)
    (htOne : t < 1)
    (hbt : b * t < 2) :
    3 * (b - 2) / (2 * (1 - t)) +
        (3 * Real.sqrt 3 / t) *
          (1 -
            (2 - b * t) /
              (2 * (Real.sqrt (1 - t)) ^ 3)) >
      3 / 2 *
        (1 +
          (1 + Real.sqrt 3) * (b - 3)) := by
  let s : ℝ := Real.sqrt (1 - t)

  have hOneMinusT :
      0 < 1 - t := by
    linarith

  have hRootPositive :
      0 < s := by
    simpa [s] using Real.sqrt_pos.2 hOneMinusT

  have hRootSquare :
      s ^ 2 = 1 - t := by
    simpa [s] using
      Real.sq_sqrt (le_of_lt hOneMinusT)

  have htFromRoot :
      t = 1 - s ^ 2 := by
    linarith [hRootSquare]

  have hRootLtOne :
      s < 1 := by
    by_contra hNot
    have hOneLe :
        1 ≤ s :=
      le_of_not_gt hNot
    have hSquareOneLe :
        1 ≤ s ^ 2 := by
      nlinarith [sq_nonneg (s - 1)]
    nlinarith [hRootSquare]

  have hOneMinusRootPositive :
      0 < 1 - s := by
    linarith

  have hRootCubePositive :
      0 < s ^ 3 :=
    pow_pos hRootPositive 3

  have hRootSquareNonnegative :
      0 ≤ s ^ 2 :=
    sq_nonneg s

  have hPolynomial :
      0 <
        s ^ 3 +
          2 * s ^ 2 +
          2 * s +
          1 := by
    nlinarith

  have hBracketIdentity :
      b * s ^ 3 +
          2 * b * s ^ 2 +
          2 * b * s +
          b -
          3 * s ^ 3 -
          6 * s ^ 2 -
          4 * s -
          2 =
        (b - 3) *
            (s ^ 3 +
              2 * s ^ 2 +
              2 * s +
              1) +
          (2 * s + 1) := by
    ring

  have hBracketPositive :
      0 <
        b * s ^ 3 +
          2 * b * s ^ 2 +
          2 * b * s +
          b -
          3 * s ^ 3 -
          6 * s ^ 2 -
          4 * s -
          2 := by
    rw [hBracketIdentity]

    have hBGapPositive :
        0 < b - 3 := by
      linarith

    have hProductPositive :
        0 <
          (b - 3) *
            (s ^ 3 +
              2 * s ^ 2 +
              2 * s +
              1) :=
      mul_pos hBGapPositive hPolynomial

    nlinarith

  have hSdenominator :
      0 < 2 * s ^ 3 :=
    mul_pos (by norm_num) hRootCubePositive

  have hQIdentity :
      (1 - (b - 3) * t / 2) -
          (2 - b * t) / (2 * s ^ 3) =
        ((1 - s) ^ 2 *
            (b * s ^ 3 +
              2 * b * s ^ 2 +
              2 * b * s +
              b -
              3 * s ^ 3 -
              6 * s ^ 2 -
              4 * s -
              2)) /
          (2 * s ^ 3) := by
    rw [htFromRoot]
    field_simp [ne_of_gt hRootPositive]
    ring

  have hQDifferencePositive :
      0 <
        (1 - (b - 3) * t / 2) -
          (2 - b * t) / (2 * s ^ 3) := by
    rw [hQIdentity]

    exact
      div_pos
        (mul_pos
          (pow_pos hOneMinusRootPositive 2)
          hBracketPositive)
        hSdenominator

  have hRootNumeratorPositive :
      0 < 2 - b * t := by
    linarith

  have hQPositive :
      0 <
        (2 - b * t) /
          (2 * s ^ 3) :=
    div_pos
      hRootNumeratorPositive
      hSdenominator

  have hQStrict :
      (2 - b * t) /
          (2 * s ^ 3) <
        1 - (b - 3) * t / 2 := by
    linarith [
      hQDifferencePositive,
      hQPositive
    ]

  have hBMinusTwoPositive :
      0 < b - 2 := by
    linarith

  have hRootIdentity :
      3 * (b - 2) / (2 * (1 - t)) -
          (3 / 2) * (b - 2) =
        3 * t * (b - 2) /
          (2 * (1 - t)) := by
    field_simp [ne_of_gt hOneMinusT]
    ring

  have hRootDenominatorPositive :
      0 < 2 * (1 - t) :=
    mul_pos (by norm_num) hOneMinusT

  have hRootDifferencePositive :
      0 <
        3 * t * (b - 2) /
          (2 * (1 - t)) := by
    exact
      div_pos
        (mul_pos
          (mul_pos (by norm_num) ht)
          hBMinusTwoPositive)
        hRootDenominatorPositive

  have hRootStrict :
      (3 / 2) * (b - 2) <
        3 * (b - 2) /
          (2 * (1 - t)) := by
    linarith [
      hRootIdentity,
      hRootDifferencePositive
    ]

  have hQGap :
      (b - 3) * t / 2 <
        1 -
          (2 - b * t) /
            (2 * s ^ 3) := by
    linarith [hQStrict]

  have hSqrtThree :
      0 < Real.sqrt 3 := by
    exact Real.sqrt_pos.2 (by norm_num)

  have hScalePositive :
      0 < 3 * Real.sqrt 3 / t := by
    exact
      div_pos
        (mul_pos (by norm_num) hSqrtThree)
        ht

  have hScaledQ :
      (3 * Real.sqrt 3 / t) *
          ((b - 3) * t / 2) <
        (3 * Real.sqrt 3 / t) *
          (1 -
            (2 - b * t) /
              (2 * s ^ 3)) :=
    mul_lt_mul_of_pos_left
      hQGap
      hScalePositive

  have hScaleIdentity :
      (3 * Real.sqrt 3 / t) *
          ((b - 3) * t / 2) =
        (3 * Real.sqrt 3 / 2) *
          (b - 3) := by
    field_simp [ne_of_gt ht]

  have hShadowStrict :
      (3 * Real.sqrt 3 / 2) *
          (b - 3) <
        (3 * Real.sqrt 3 / t) *
          (1 -
            (2 - b * t) /
              (2 * s ^ 3)) := by
    calc
      (3 * Real.sqrt 3 / 2) *
            (b - 3) =
          (3 * Real.sqrt 3 / t) *
            ((b - 3) * t / 2) :=
        hScaleIdentity.symm
      _ <
          (3 * Real.sqrt 3 / t) *
            (1 -
              (2 - b * t) /
                (2 * s ^ 3)) :=
        hScaledQ

  have hLinearIdentity :
      (3 / 2) * (b - 2) +
          (3 * Real.sqrt 3 / 2) *
            (b - 3) =
        3 / 2 *
          (1 +
            (1 + Real.sqrt 3) *
              (b - 3)) := by
    ring

  have hTotal :
      (3 / 2) * (b - 2) +
          (3 * Real.sqrt 3 / 2) *
            (b - 3) <
        3 * (b - 2) /
            (2 * (1 - t)) +
          (3 * Real.sqrt 3 / t) *
            (1 -
              (2 - b * t) /
                (2 * s ^ 3)) :=
    add_lt_add hRootStrict hShadowStrict

  calc
    3 / 2 *
          (1 +
            (1 + Real.sqrt 3) *
              (b - 3)) =
        (3 / 2) * (b - 2) +
          (3 * Real.sqrt 3 / 2) *
            (b - 3) :=
      hLinearIdentity.symm
    _ <
        3 * (b - 2) /
            (2 * (1 - t)) +
          (3 * Real.sqrt 3 / t) *
            (1 -
              (2 - b * t) /
                (2 * s ^ 3)) :=
      hTotal
    _ =
        3 * (b - 2) /
            (2 * (1 - t)) +
          (3 * Real.sqrt 3 / t) *
            (1 -
              (2 - b * t) /
                (2 * (Real.sqrt (1 - t)) ^ 3)) := by
      rfl



/--
For every `0 < t < 1`, the exact constant-negative-defect nonlinear
quantity differs from its first-order comparison value by an explicit
algebraic remainder.

This is an identity only; positivity and optimization are separate
consequences.
-/
theorem schwarzschildConstantNegativeDefect_Kminus_sub_Klin_exact
    (b t : ℝ)
    (ht : 0 < t)
    (htOne : t < 1) :
    (3 * (b - 2) / (2 * (1 - t)) +
        (3 * Real.sqrt 3 / t) *
          (1 -
            (2 - b * t) /
              (2 * (Real.sqrt (1 - t)) ^ 3))) -
      3 / 2 *
        (1 +
          (1 + Real.sqrt 3) * (b - 3)) =
    3 * t * (b - 2) /
        (2 * (1 - t)) +
      (3 * Real.sqrt 3 / t) *
        (((1 - Real.sqrt (1 - t)) ^ 2 *
            (b * (Real.sqrt (1 - t)) ^ 3 +
              2 * b * (Real.sqrt (1 - t)) ^ 2 +
              2 * b * Real.sqrt (1 - t) +
              b -
              3 * (Real.sqrt (1 - t)) ^ 3 -
              6 * (Real.sqrt (1 - t)) ^ 2 -
              4 * Real.sqrt (1 - t) -
              2)) /
          (2 * (Real.sqrt (1 - t)) ^ 3)) := by
  set s : ℝ := Real.sqrt (1 - t) with hsDef

  have hOneMinusT :
      0 < 1 - t := by
    linarith

  have hsPositive :
      0 < s := by
    rw [hsDef]
    exact Real.sqrt_pos.2 hOneMinusT

  have hsSquare :
      s ^ 2 = 1 - t := by
    rw [hsDef]
    exact Real.sq_sqrt (le_of_lt hOneMinusT)

  have htFromRoot :
      t = 1 - s ^ 2 := by
    linarith [hsSquare]

  have hRootTimeNonzero :
      1 - s ^ 2 ≠ 0 := by
    rw [← htFromRoot]
    exact ne_of_gt ht

  rw [htFromRoot]
  field_simp [
    ne_of_gt hsPositive,
    hRootTimeNonzero
  ]
  ring

/--
The admissible parameter domain for the constant negative-defect
Schwarzschild photon model.
-/
def schwarzschildConstantNegativeDefectAdmissible
    (b t : ℝ) : Prop :=
  3 < b ∧
    0 < t ∧
    t < 1 ∧
    b * t < 2

/--
The exact nonlinear-minus-linear gap for the constant negative-defect
Schwarzschild photon-shadow model.
-/
def schwarzschildConstantNegativeDefectGap
    (b t : ℝ) : ℝ :=
  3 * (b - 2) / (2 * (1 - t)) +
      (3 * Real.sqrt 3 / t) *
        (1 -
          (2 - b * t) /
            (2 * (Real.sqrt (1 - t)) ^ 3)) -
    3 / 2 *
      (1 +
        (1 + Real.sqrt 3) * (b - 3))

/--
Exact positive-factor form of the constant negative-defect gap.
-/
theorem schwarzschildConstantNegativeDefectGap_factorization
    (b t : ℝ)
    (ht : 0 < t)
    (htOne : t < 1) :
    schwarzschildConstantNegativeDefectGap b t =
      3 * (1 - Real.sqrt (1 - t)) /
          (2 * (Real.sqrt (1 - t)) ^ 3 *
            (1 + Real.sqrt (1 - t))) *
        ((b - 2) *
            Real.sqrt (1 - t) *
            (1 + Real.sqrt (1 - t)) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                ((Real.sqrt (1 - t)) ^ 3 +
                  2 * (Real.sqrt (1 - t)) ^ 2 +
                  2 * Real.sqrt (1 - t) +
                  1) +
              (2 * Real.sqrt (1 - t) + 1))) := by
  let s : ℝ := Real.sqrt (1 - t)

  have hOneMinusT :
      0 < 1 - t := by
    linarith

  have hSPos :
      0 < s := by
    simpa [s] using Real.sqrt_pos.2 hOneMinusT

  have hSSquare :
      s ^ 2 = 1 - t := by
    simpa [s] using
      Real.sq_sqrt (le_of_lt hOneMinusT)

  have hTFromS :
      t = 1 - s ^ 2 := by
    linarith [hSSquare]

  have hSNe :
      s ≠ 0 :=
    ne_of_gt hSPos

  have hOnePlusSNe :
      1 + s ≠ 0 := by
    nlinarith

  have hTFormPos :
      0 < 1 - s ^ 2 := by
    rw [← hTFromS]
    exact ht

  have hTFormNe :
      1 - s ^ 2 ≠ 0 :=
    ne_of_gt hTFormPos

  change
    3 * (b - 2) / (2 * (1 - t)) +
          (3 * Real.sqrt 3 / t) *
            (1 -
              (2 - b * t) /
                (2 * s ^ 3)) -
        3 / 2 *
          (1 +
            (1 + Real.sqrt 3) * (b - 3)) =
      3 * (1 - s) /
          (2 * s ^ 3 * (1 + s)) *
        ((b - 2) * s * (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1)))

  rw [hTFromS]
  field_simp [
    hSNe,
    hOnePlusSNe,
    hTFormNe
  ] <;> ring


/--
The exact gap strictly dominates one half of the product `b * t`
throughout the admissible domain.
-/
theorem schwarzschildConstantNegativeDefectGap_half_mul_lt
    (b t : ℝ)
    (hAdmissible :
      schwarzschildConstantNegativeDefectAdmissible b t) :
    b * t / 2 <
      schwarzschildConstantNegativeDefectGap b t := by
  rcases hAdmissible with
    ⟨hb, ht, htOne, hbt⟩

  let s : ℝ := Real.sqrt (1 - t)

  have hOneMinusT :
      0 < 1 - t := by
    linarith

  have hSPos :
      0 < s := by
    simpa [s] using Real.sqrt_pos.2 hOneMinusT

  have hSSquare :
      s ^ 2 = 1 - t := by
    simpa [s] using
      Real.sq_sqrt (le_of_lt hOneMinusT)

  have hTFromS :
      t = 1 - s ^ 2 := by
    linarith [hSSquare]

  have hSLtOne :
      s < 1 := by
    by_contra hNot
    have hOneLeS :
        1 ≤ s :=
      le_of_not_gt hNot
    have hSquareOneLe :
        1 ≤ s ^ 2 := by
      nlinarith [sq_nonneg (s - 1)]
    nlinarith [hSSquare]

  have hOneMinusSPos :
      0 < 1 - s := by
    linarith

  have hOnePlusSPos :
      0 < 1 + s := by
    linarith

  have hSNe :
      s ≠ 0 :=
    ne_of_gt hSPos

  have hOnePlusSNe :
      1 + s ≠ 0 :=
    ne_of_gt hOnePlusSPos

  have hSSquareLtOne :
      s ^ 2 < 1 := by
    rw [hSSquare]
    linarith

  have hBPos :
      0 < b := by
    linarith

  have hBSquareLt :
      b * s ^ 2 < b := by
    simpa using
      mul_lt_mul_of_pos_left
        hSSquareLtOne
        hBPos

  have hCoefficientPos :
      0 <
        3 * (b - 2) -
          b * s ^ 2 := by
    nlinarith

  have hPolynomialPos :
      0 <
        s ^ 3 +
          2 * s ^ 2 +
          2 * s +
          1 := by
    nlinarith [
      pow_pos hSPos 3,
      sq_nonneg s
    ]

  have hBGapPos :
      0 < b - 3 := by
    linarith

  have hBracketTailPos :
      0 <
        (b - 3) *
            (s ^ 3 +
              2 * s ^ 2 +
              2 * s +
              1) +
          (2 * s + 1) := by
    exact
      add_pos
        (mul_pos
          hBGapPos
          hPolynomialPos)
        (by linarith)

  have hSqrtThreePos :
      0 < Real.sqrt 3 := by
    exact Real.sqrt_pos.2 (by norm_num)

  have hLargeBracketPos :
      0 <
        s * (1 + s) ^ 2 *
            (3 * (b - 2) -
              b * s ^ 2) +
          3 * Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1)) := by
    exact
      add_pos
        (mul_pos
          (mul_pos
            hSPos
            (pow_pos hOnePlusSPos 2))
          hCoefficientPos)
        (mul_pos
          (mul_pos
            (by norm_num)
            hSqrtThreePos)
          hBracketTailPos)

  have hDenominatorPos :
      0 <
        2 * s ^ 3 * (1 + s) := by
    exact
      mul_pos
        (mul_pos
          (by norm_num)
          (pow_pos hSPos 3))
        hOnePlusSPos

  have hPrefactorPos :
      0 <
        (1 - s) /
          (2 * s ^ 3 * (1 + s)) :=
    div_pos
      hOneMinusSPos
      hDenominatorPos

  have hFactorization :=
    schwarzschildConstantNegativeDefectGap_factorization
      b
      t
      ht
      htOne

  change
    schwarzschildConstantNegativeDefectGap b t =
      3 * (1 - s) /
          (2 * s ^ 3 * (1 + s)) *
        ((b - 2) * s * (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1))) at hFactorization

  have hDifference :
      schwarzschildConstantNegativeDefectGap b t -
          b * t / 2 =
        (1 - s) /
            (2 * s ^ 3 * (1 + s)) *
          (s * (1 + s) ^ 2 *
              (3 * (b - 2) -
                b * s ^ 2) +
            3 * Real.sqrt 3 *
              ((b - 3) *
                  (s ^ 3 +
                    2 * s ^ 2 +
                    2 * s +
                    1) +
                (2 * s + 1))) := by
    rw [hFactorization, hTFromS]
    field_simp [
      hSNe,
      hOnePlusSNe
    ] <;> ring

  have hDifferencePos :
      0 <
        schwarzschildConstantNegativeDefectGap b t -
          b * t / 2 := by
    rw [hDifference]
    exact
      mul_pos
        hPrefactorPos
        hLargeBracketPos

  linarith



set_option maxHeartbeats 1000000 in
/--
A uniform product-scale upper bound for the exact gap throughout the
admissible domain.
-/
theorem schwarzschildConstantNegativeDefectGap_le_192_mul
    (b t : ℝ)
    (hAdmissible :
      schwarzschildConstantNegativeDefectAdmissible b t) :
    schwarzschildConstantNegativeDefectGap b t
      ≤ 192 * (b * t) := by
  rcases hAdmissible with
    ⟨hb, ht, htOne, hbt⟩

  let s : ℝ := Real.sqrt (1 - t)

  have hOneMinusT :
      0 < 1 - t := by
    linarith

  have hSPos :
      0 < s := by
    simpa [s] using Real.sqrt_pos.2 hOneMinusT

  have hSNonneg :
      0 ≤ s :=
    le_of_lt hSPos

  have hSSquare :
      s ^ 2 = 1 - t := by
    simpa [s] using
      Real.sq_sqrt (le_of_lt hOneMinusT)

  have hTFromS :
      t = 1 - s ^ 2 := by
    linarith [hSSquare]

  have hSLtOne :
      s < 1 := by
    by_contra hNot
    have hOneLeS :
        1 ≤ s :=
      le_of_not_gt hNot
    have hSquareOneLe :
        1 ≤ s ^ 2 := by
      nlinarith [sq_nonneg (s - 1)]
    nlinarith [hSSquare]

  have hSLeOne :
      s ≤ 1 :=
    le_of_lt hSLtOne

  have hOneMinusSPos :
      0 < 1 - s := by
    linarith

  have hOnePlusSPos :
      0 < 1 + s := by
    linarith

  have hThreeT :
      3 * t < b * t :=
    mul_lt_mul_of_pos_right hb ht

  have hTLtTwoThirds :
      t < (2 : ℝ) / 3 := by
    nlinarith

  have hOneThird :
      (1 : ℝ) / 3 < 1 - t := by
    linarith

  have hSHalf :
      (1 : ℝ) / 2 < s := by
    by_contra hNot
    have hSLeHalf :
        s ≤ (1 : ℝ) / 2 :=
      le_of_not_gt hNot
    have hSquareLeQuarter :
        s ^ 2 ≤ (1 : ℝ) / 4 := by
      have hAux :
          0 ≤
            ((1 : ℝ) / 2 - s) *
              ((1 : ℝ) / 2 + s) :=
        mul_nonneg
          (by linarith)
          (by linarith)
      nlinarith [hAux]
    nlinarith [hSSquare, hOneThird]

  have hCubeAux :
      0 <
        (s - (1 : ℝ) / 2) *
          (s ^ 2 +
            s / 2 +
            (1 : ℝ) / 4) := by
    exact
      mul_pos
        (by linarith)
        (by nlinarith [sq_nonneg s])

  have hSCubeEighth :
      (1 : ℝ) / 8 < s ^ 3 := by
    nlinarith [hCubeAux]

  have hTwoCubeQuarter :
      (1 : ℝ) / 4 <
        2 * s ^ 3 := by
    nlinarith

  have hTwoCubePos :
      0 < 2 * s ^ 3 := by
    exact
      mul_pos
        (by norm_num)
        (pow_pos hSPos 3)

  have hOneLtOnePlusS :
      1 < 1 + s := by
    linarith

  have hDenominatorGrowth :
      2 * s ^ 3 <
        2 * s ^ 3 * (1 + s) := by
    simpa using
      mul_lt_mul_of_pos_left
        hOneLtOnePlusS
        hTwoCubePos

  have hDenominatorQuarter :
      (1 : ℝ) / 4 <
        2 * s ^ 3 * (1 + s) :=
    lt_trans hTwoCubeQuarter hDenominatorGrowth

  have hDenominatorPos :
      0 <
        2 * s ^ 3 * (1 + s) := by
    linarith

  have hOneMinusSLeT :
      1 - s ≤ t := by
    have hProductPos :
        0 < s * (1 - s) :=
      mul_pos hSPos hOneMinusSPos
    nlinarith [hTFromS]

  have hNumeratorLe :
      3 * (1 - s) ≤ 3 * t := by
    nlinarith

  have hQuarterLe :
      (1 : ℝ) / 4 ≤
        2 * s ^ 3 * (1 + s) :=
    le_of_lt hDenominatorQuarter

  have hScaledDenominator :
      3 * t ≤
        12 * t *
          (2 * s ^ 3 * (1 + s)) := by
    have hScaled :=
      mul_le_mul_of_nonneg_left
        hQuarterLe
        (show 0 ≤ 12 * t by positivity)
    nlinarith [hScaled]

  have hPrefactorNumeratorLe :
      3 * (1 - s) ≤
        12 * t *
          (2 * s ^ 3 * (1 + s)) :=
    le_trans hNumeratorLe hScaledDenominator

  have hPrefactorLe :
      3 * (1 - s) /
          (2 * s ^ 3 * (1 + s))
        ≤ 12 * t := by
    exact
      (div_le_iff₀ hDenominatorPos).2
        hPrefactorNumeratorLe

  have hOnePlusSquareLeFour :
      (1 + s) ^ 2 ≤ 4 := by
    nlinarith [sq_nonneg (1 - s)]

  have hRadialFactorLeFour :
      s * (1 + s) ^ 2 ≤ 4 := by
    calc
      s * (1 + s) ^ 2
          ≤ 1 * (1 + s) ^ 2 := by
            exact
              mul_le_mul_of_nonneg_right
                hSLeOne
                (sq_nonneg (1 + s))
      _ ≤ 1 * 4 := by
            exact
              mul_le_mul_of_nonneg_left
                hOnePlusSquareLeFour
                (by norm_num)
      _ = 4 := by
            norm_num

  have hOneMinusSNonneg :
      0 ≤ 1 - s := by
    linarith

  have hOnePlusSNonneg :
      0 ≤ 1 + s :=
    le_of_lt hOnePlusSPos

  have hSSquareLeOne :
      s ^ 2 ≤ 1 := by
    have hAux :
        0 ≤
          (1 - s) * (1 + s) :=
      mul_nonneg hOneMinusSNonneg hOnePlusSNonneg
    nlinarith [hAux]

  have hSCubeLeOne :
      s ^ 3 ≤ 1 := by
    have hAux :=
      mul_le_mul_of_nonneg_left
        hSSquareLeOne
        hSNonneg
    nlinarith [hAux, hSLeOne]

  have hPolynomialLeSix :
      s ^ 3 +
          2 * s ^ 2 +
          2 * s +
          1
        ≤ 6 := by
    nlinarith [
      hSCubeLeOne,
      hSSquareLeOne,
      hSLeOne
    ]

  have hPolynomialPos :
      0 <
        s ^ 3 +
          2 * s ^ 2 +
          2 * s +
          1 := by
    nlinarith [
      pow_pos hSPos 3,
      sq_nonneg s
    ]

  have hBGapNonneg :
      0 ≤ b - 3 := by
    linarith

  have hBMinusTwoNonneg :
      0 ≤ b - 2 := by
    linarith

  have hPolynomialScaled :=
    mul_le_mul_of_nonneg_left
      hPolynomialLeSix
      hBGapNonneg

  have hLinearTailLe :
      2 * s + 1 ≤ 3 := by
    linarith

  have hTailLeSixB :
      (b - 3) *
            (s ^ 3 +
              2 * s ^ 2 +
              2 * s +
              1) +
          (2 * s + 1)
        ≤ 6 * b := by
    nlinarith [
      hPolynomialScaled,
      hLinearTailLe
    ]

  have hTailNonneg :
      0 ≤
        (b - 3) *
            (s ^ 3 +
              2 * s ^ 2 +
              2 * s +
              1) +
          (2 * s + 1) := by
    exact
      le_of_lt
        (add_pos
          (mul_pos
            (by linarith)
            hPolynomialPos)
          (by linarith))

  have hRadialTermScaled :=
    mul_le_mul_of_nonneg_left
      hRadialFactorLeFour
      hBMinusTwoNonneg

  have hRadialTermLeFourB :
      (b - 2) *
          (s * (1 + s) ^ 2)
        ≤ 4 * b := by
    nlinarith [hRadialTermScaled]

  have hSqrtThreeNonneg :
      0 ≤ Real.sqrt 3 :=
    Real.sqrt_nonneg 3

  have hSqrtThreeSquare :
      (Real.sqrt 3) ^ 2 = 3 := by
    simpa using
      Real.sq_sqrt
        (show (0 : ℝ) ≤ 3 by norm_num)

  have hSqrtThreeLeTwo :
      Real.sqrt 3 ≤ 2 := by
    nlinarith [
      hSqrtThreeNonneg,
      hSqrtThreeSquare
    ]

  have hSqrtTailStep :=
    mul_le_mul_of_nonneg_right
      hSqrtThreeLeTwo
      hTailNonneg

  have hTwiceTailStep :=
    mul_le_mul_of_nonneg_left
      hTailLeSixB
      (show (0 : ℝ) ≤ 2 by norm_num)

  have hSqrtTailLeTwelveB :
      Real.sqrt 3 *
          ((b - 3) *
              (s ^ 3 +
                2 * s ^ 2 +
                2 * s +
                1) +
            (2 * s + 1))
        ≤ 12 * b := by
    nlinarith [
      hSqrtTailStep,
      hTwiceTailStep
    ]

  have hBracketLe :
      (b - 2) *
            s *
            (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1))
        ≤ 16 * b := by
    nlinarith [
      hRadialTermLeFourB,
      hSqrtTailLeTwelveB
    ]

  have hBracketNonneg :
      0 ≤
        (b - 2) *
            s *
            (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1)) := by
    exact
      add_nonneg
        (mul_nonneg
          (mul_nonneg
            hBMinusTwoNonneg
            hSNonneg)
          (sq_nonneg (1 + s)))
        (mul_nonneg
          hSqrtThreeNonneg
          hTailNonneg)

  rw [
    schwarzschildConstantNegativeDefectGap_factorization
      b
      t
      ht
      htOne
  ]

  change
    3 * (1 - s) /
          (2 * s ^ 3 * (1 + s)) *
        ((b - 2) *
            s *
            (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1)))
      ≤ 192 * (b * t)

  calc
    3 * (1 - s) /
          (2 * s ^ 3 * (1 + s)) *
        ((b - 2) *
            s *
            (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1)))
        ≤
      (12 * t) *
        ((b - 2) *
            s *
            (1 + s) ^ 2 +
          Real.sqrt 3 *
            ((b - 3) *
                (s ^ 3 +
                  2 * s ^ 2 +
                  2 * s +
                  1) +
              (2 * s + 1))) := by
          exact
            mul_le_mul_of_nonneg_right
              hPrefactorLe
              hBracketNonneg
    _ ≤
      (12 * t) * (16 * b) := by
          exact
            mul_le_mul_of_nonneg_left
              hBracketLe
              (show 0 ≤ 12 * t by positivity)
    _ = 192 * (b * t) := by
          ring


/--
Elementary epsilon formulation of convergence of a real sequence to
zero.
-/
def schwarzschildSequenceTendsToZero
    (u : ℕ → ℝ) : Prop :=
  ∀ ε : ℝ,
    0 < ε →
      ∃ N : ℕ,
        ∀ n : ℕ,
          N ≤ n →
            |u n| < ε

/--
The explicit sequence `bₙ = 4`.
-/
def schwarzschildConstantNegativeDefectInfimizingB
    (_n : ℕ) : ℝ :=
  4


/--
The explicit sequence `tₙ = 1 / (n + 3)`.
-/
def schwarzschildConstantNegativeDefectInfimizingT
    (n : ℕ) : ℝ :=
  1 / ((n : ℝ) + 3)



/--
Every pair `bₙ = 4`, `tₙ = 1 / (n + 3)` belongs to the admissible
constant negative-defect domain.
-/
theorem schwarzschildConstantNegativeDefect_infimizing_admissible
    (n : ℕ) :
    schwarzschildConstantNegativeDefectAdmissible
      (schwarzschildConstantNegativeDefectInfimizingB n)
      (schwarzschildConstantNegativeDefectInfimizingT n) := by
  have hn :
      0 ≤ (n : ℝ) := by
    positivity

  have hDenominatorPos :
      0 < (n : ℝ) + 3 := by
    positivity

  unfold
    schwarzschildConstantNegativeDefectAdmissible
    schwarzschildConstantNegativeDefectInfimizingB
    schwarzschildConstantNegativeDefectInfimizingT

  constructor
  · norm_num
  constructor
  · exact one_div_pos.mpr hDenominatorPos
  constructor
  · exact
      (div_lt_one hDenominatorPos).2
        (by nlinarith [hn])
  · have hDiv :
        4 / ((n : ℝ) + 3) < 2 := by
      exact
        (div_lt_iff₀ hDenominatorPos).2
          (by nlinarith [hn])

    simpa [div_eq_mul_inv] using hDiv


/--
The explicit products `bₙ tₙ = 4 / (n + 3)` converge to zero.
-/
theorem schwarzschildConstantNegativeDefect_infimizing_product_tendsToZero :
    schwarzschildSequenceTendsToZero
      (fun n : ℕ =>
        schwarzschildConstantNegativeDefectInfimizingB n *
          schwarzschildConstantNegativeDefectInfimizingT n) := by
  unfold schwarzschildSequenceTendsToZero

  intro ε hε

  obtain ⟨N, hN⟩ :=
    exists_nat_gt (4 / ε)

  refine ⟨N, ?_⟩
  intro n hn

  have hNLeN :
      (N : ℝ) ≤ (n : ℝ) := by
    exact_mod_cast hn

  have hDenominatorPos :
      0 < (n : ℝ) + 3 := by
    positivity

  have hLarge :
      4 / ε < (n : ℝ) + 3 := by
    calc
      4 / ε < (N : ℝ) :=
        hN
      _ ≤ (n : ℝ) :=
        hNLeN
      _ < (n : ℝ) + 3 := by
        linarith

  have hCross :
      4 < ((n : ℝ) + 3) * ε :=
    (div_lt_iff₀ hε).1 hLarge

  have hFour :
      4 < ε * ((n : ℝ) + 3) := by
    nlinarith [hCross]

  have hFraction :
      4 / ((n : ℝ) + 3) < ε := by
    apply (div_lt_iff₀ hDenominatorPos).2
    nlinarith [hFour]

  have hProductPos :
      0 <
        schwarzschildConstantNegativeDefectInfimizingB n *
          schwarzschildConstantNegativeDefectInfimizingT n := by
    exact
      mul_pos
        (by
          unfold
            schwarzschildConstantNegativeDefectInfimizingB
          norm_num)
        (by
          unfold
            schwarzschildConstantNegativeDefectInfimizingT
          exact one_div_pos.mpr hDenominatorPos)

  rw [abs_of_pos hProductPos]

  simpa [
    schwarzschildConstantNegativeDefectInfimizingB,
    schwarzschildConstantNegativeDefectInfimizingT,
    div_eq_mul_inv
  ] using hFraction

/--
For every admissible sequence, the exact gaps converge to zero if and
only if the products `bₙ tₙ` converge to zero.
-/
theorem schwarzschildConstantNegativeDefect_infimizingSequence_iff
    (b t : ℕ → ℝ)
    (hAdmissible :
      ∀ n : ℕ,
        schwarzschildConstantNegativeDefectAdmissible
          (b n)
          (t n)) :
    schwarzschildSequenceTendsToZero
        (fun n : ℕ =>
          schwarzschildConstantNegativeDefectGap
            (b n)
            (t n))
      ↔
    schwarzschildSequenceTendsToZero
        (fun n : ℕ =>
          b n * t n) := by
  unfold schwarzschildSequenceTendsToZero

  constructor
  · intro hGap ε hε

    obtain ⟨N, hN⟩ :=
      hGap
        (ε / 2)
        (by linarith)

    refine ⟨N, ?_⟩
    intro n hn

    rcases hAdmissible n with
      ⟨hb, ht, htOne, hbt⟩

    have hDomain :
        schwarzschildConstantNegativeDefectAdmissible
          (b n)
          (t n) :=
      ⟨hb, ht, htOne, hbt⟩

    have hLower :=
      schwarzschildConstantNegativeDefectGap_half_mul_lt
        (b n)
        (t n)
        hDomain

    have hProductPos :
        0 < b n * t n :=
      mul_pos
        (by linarith)
        ht

    have hGapPos :
        0 <
          schwarzschildConstantNegativeDefectGap
            (b n)
            (t n) := by
      nlinarith [hLower, hProductPos]

    have hSmall :=
      hN n hn

    rw [abs_of_pos hGapPos] at hSmall
    rw [abs_of_pos hProductPos]

    nlinarith [hLower, hSmall]

  · intro hProduct ε hε

    obtain ⟨N, hN⟩ :=
      hProduct
        (ε / 192)
        (by positivity)

    refine ⟨N, ?_⟩
    intro n hn

    rcases hAdmissible n with
      ⟨hb, ht, htOne, hbt⟩

    have hDomain :
        schwarzschildConstantNegativeDefectAdmissible
          (b n)
          (t n) :=
      ⟨hb, ht, htOne, hbt⟩

    have hLower :=
      schwarzschildConstantNegativeDefectGap_half_mul_lt
        (b n)
        (t n)
        hDomain

    have hUpper :=
      schwarzschildConstantNegativeDefectGap_le_192_mul
        (b n)
        (t n)
        hDomain

    have hProductPos :
        0 < b n * t n :=
      mul_pos
        (by linarith)
        ht

    have hGapPos :
        0 <
          schwarzschildConstantNegativeDefectGap
            (b n)
            (t n) := by
      nlinarith [hLower, hProductPos]

    have hSmall :=
      hN n hn

    rw [abs_of_pos hProductPos] at hSmall
    rw [abs_of_pos hGapPos]

    nlinarith [hUpper, hSmall]

end

end Frontier
end Chronos
