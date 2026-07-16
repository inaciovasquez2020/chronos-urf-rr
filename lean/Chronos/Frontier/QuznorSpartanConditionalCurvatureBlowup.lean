import Mathlib

namespace Chronos.Frontier

open Filter

/--
The five pieces of charge-and-low-multipole data held fixed in the
conditional Spartan theorem.
-/
structure QuznorSpartanFixedFiberData where
  s2 : ℝ
  s3 : Fin 4 → ℝ
  s4 : Matrix (Fin 4) (Fin 4) ℝ
  q1 : ℝ
  q5 : ℝ

/--
A conditional certificate for the Spartan curvature-blowup implication.

The structure does not prove profile-scale convergence, endpoint-ratio
limits, the six-dimensional curvature identity, or higher-derivative
control.
-/
structure QuznorSpartanConditionalCurvatureBlowupData where
  fiberData : ℕ → QuznorSpartanFixedFiberData
  fixedFiberData : QuznorSpartanFixedFiberData
  fiberData_fixed :
    ∀ n : ℕ, fiberData n = fixedFiberData
  scalarCurvatureAtSample : ℕ → ℝ
  scalarCurvatureSup : ℕ → ℝ
  sample_le_sup :
    ∀ n : ℕ,
      scalarCurvatureAtSample n ≤ scalarCurvatureSup n
  c0 : ℝ
  c0_pos : 0 < c0
  normalizedSampleTendsto :
    Tendsto
      (fun n : ℕ =>
        scalarCurvatureAtSample n / (n : ℝ))
      atTop
      (nhds c0)

/-- The certificate preserves one fixed abstract fiber. -/
theorem quznorSpartanConditionalFiber_fixed
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    ∀ n : ℕ, data.fiberData n = data.fixedFiberData :=
  data.fiberData_fixed

/--
A positive normalized sampled-curvature limit forces sampled curvature
to diverge to positive infinity.
-/
theorem quznorSpartanConditionalSampleCurvature_tendsto_atTop
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    Tendsto data.scalarCurvatureAtSample atTop atTop := by
  exact Filter.Tendsto.num
    (f := data.scalarCurvatureAtSample)
    (g := fun n : ℕ => (n : ℝ))
    (l := atTop)
    tendsto_natCast_atTop_atTop
    data.c0_pos
    data.normalizedSampleTendsto

/--
The curvature supremum diverges because it dominates the sampled
curvature pointwise.
-/
theorem quznorSpartanConditionalCurvatureSup_tendsto_atTop
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    Tendsto data.scalarCurvatureSup atTop atTop := by
  exact Filter.tendsto_atTop_mono
    data.sample_le_sup
    (quznorSpartanConditionalSampleCurvature_tendsto_atTop data)

/--
Spartan Theorem — conditional Lean package.

The theorem does not discharge the analytic or supergravity hypotheses
stored in the certificate.
-/
theorem quznorSpartanConditionalCurvatureBlowup
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    (∀ n : ℕ,
      data.fiberData n = data.fixedFiberData) ∧
    Tendsto data.scalarCurvatureSup atTop atTop := by
  exact ⟨
    quznorSpartanConditionalFiber_fixed data,
    quznorSpartanConditionalCurvatureSup_tendsto_atTop data
  ⟩


/--
Private unit-circle power-chord estimate.

For a complex number of unit norm, the chord from `1` to its `N`th
power is bounded by `N` times the original chord.
-/
private theorem quznorSpartan_unitCircle_powChord_le
    (z : ℂ)
    (N : ℕ)
    (hz : ‖z‖ = 1) :
    ‖z ^ N - 1‖ ≤ (N : ℝ) * ‖z - 1‖ := by
  induction N with
  | zero =>
      simp
  | succ N ih =>
      have hdecomp :
          z ^ (N + 1) - 1 =
            z ^ N * (z - 1) + (z ^ N - 1) := by
        rw [pow_succ]
        ring
      rw [hdecomp]
      calc
        ‖z ^ N * (z - 1) + (z ^ N - 1)‖
            ≤ ‖z ^ N * (z - 1)‖ + ‖z ^ N - 1‖ :=
          norm_add_le _ _
        _ =
            ‖z ^ N‖ * ‖z - 1‖ + ‖z ^ N - 1‖ := by
          rw [norm_mul]
        _ ≤
            ‖z ^ N‖ * ‖z - 1‖ +
              (N : ℝ) * ‖z - 1‖ := by
          exact add_le_add_right ih _
        _ =
            (((N + 1 : ℕ) : ℝ)) * ‖z - 1‖ := by
          rw [norm_pow, hz, one_pow, one_mul]
          push_cast
          ring

/--
Spartan complex-exponential chord lemma.

For every real `u` and positive natural number `N`,

`‖exp(iu) - 1‖ ≤ N * ‖exp(iu/N) - 1‖`.
-/
theorem quznorSpartan_expChord_nat_mul_le
    (u : ℝ)
    (N : ℕ)
    (hN : 0 < N) :
    ‖Complex.exp (Complex.I * (u : ℂ)) - 1‖
      ≤
    (N : ℝ) *
      ‖Complex.exp
          (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ := by
  let z : ℂ :=
    Complex.exp
      (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ))
  have hz : ‖z‖ = 1 := by
    dsimp [z]
    simpa using
      Complex.norm_exp_I_mul_ofReal (u / (N : ℝ))
  have hpow :
      z ^ N =
        Complex.exp (Complex.I * (u : ℂ)) := by
    dsimp [z]
    rw [← Complex.exp_nat_mul]
    congr 1
    have hN0R : (N : ℝ) ≠ 0 := by
      exact_mod_cast hN.ne'
    have hN0C : (N : ℂ) ≠ 0 := by
      exact_mod_cast hN.ne'
    push_cast
    field_simp [hN0R, hN0C]
  have h :=
    quznorSpartan_unitCircle_powChord_le z N hz
  rw [hpow] at h
  simpa [z] using h

/-- Spartan normalized lower chord bound.

For every real `u` and positive natural number `N`, if `|u| ≤ π N`, then
`2 |u| / (π N) ≤ ‖exp(iu/N) - 1‖`.
-/
theorem quznorSpartan_normalizedLowerChord_le
    (u : ℝ) (N : ℕ) (hN : 0 < N)
    (hu : |u| ≤ Real.pi * (N : ℝ)) :
    2 * |u| / (Real.pi * (N : ℝ)) ≤
      ‖Complex.exp
          (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ := by
  have hNpos : 0 < (N : ℝ) := by
    exact_mod_cast hN
  have hu_div : |u / (N : ℝ)| ≤ Real.pi := by
    rw [abs_div, abs_of_pos hNpos]
    exact (div_le_iff₀ hNpos).2 hu
  have hhalf : |u / (N : ℝ) / 2| ≤ Real.pi / 2 := by
    rw [abs_div]
    norm_num
    linarith
  have hs :
      2 / Real.pi * |u / (N : ℝ) / 2| ≤
        |Real.sin (u / (N : ℝ) / 2)| :=
    Real.mul_abs_le_abs_sin hhalf
  rw [Complex.norm_exp_I_mul_ofReal_sub_one]
  calc
    2 * |u| / (Real.pi * (N : ℝ))
        = 2 * (2 / Real.pi * |u / (N : ℝ) / 2|) := by
            rw [abs_div, abs_div, abs_of_pos hNpos]
            norm_num
            ring
    _ ≤ 2 * |Real.sin (u / (N : ℝ) / 2)| :=
      mul_le_mul_of_nonneg_left hs (by norm_num)
    _ = ‖2 * Real.sin (u / (N : ℝ) / 2)‖ := by
      rw [Real.norm_eq_abs, abs_mul]
      norm_num

/-- Uniform lower bound for the scaled Spartan exponential chord.

The factor `N` cancels the normalization loss in the lower chord estimate:
if `|u| ≤ π N`, then `2 |u| / π ≤ N ‖exp(iu/N) - 1‖`.
-/
theorem quznorSpartan_scaledChord_uniformLowerBound
    (u : ℝ) (N : ℕ) (hN : 0 < N)
    (hu : |u| ≤ Real.pi * (N : ℝ)) :
    2 * |u| / Real.pi ≤
      (N : ℝ) *
        ‖Complex.exp
            (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ := by
  have hNpos : 0 < (N : ℝ) := by
    exact_mod_cast hN
  have hLower :=
    quznorSpartan_normalizedLowerChord_le u N hN hu
  apply (div_le_iff₀ Real.pi_pos).2
  have hCleared :
      2 * |u| ≤
        ‖Complex.exp
            (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ *
          (Real.pi * (N : ℝ)) :=
    (div_le_iff₀ (mul_pos Real.pi_pos hNpos)).1 hLower
  calc
    2 * |u| ≤
        ‖Complex.exp
            (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ *
          (Real.pi * (N : ℝ)) := hCleared
    _ =
        (N : ℝ) *
          ‖Complex.exp
              (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1‖ *
            Real.pi := by
      ring

/-- Abstract reverse-triangle coercivity.

A main term with norm at least `lower`, perturbed by a remainder with norm at
most `error`, retains norm at least `lower - error`.
-/
theorem quznorSpartan_reverseTriangle_coercivity
    {E : Type*} [SeminormedAddCommGroup E]
    (mainTerm remainder : E) (lower error : ℝ)
    (hmain : lower ≤ ‖mainTerm‖)
    (hremainder : ‖remainder‖ ≤ error) :
    lower - error ≤ ‖mainTerm + remainder‖ := by
  have htriangle :
      ‖mainTerm‖ ≤ ‖mainTerm + remainder‖ + ‖remainder‖ := by
    calc
      ‖mainTerm‖ = ‖mainTerm + remainder - remainder‖ := by
        congr 1
        abel
      _ ≤ ‖mainTerm + remainder‖ + ‖remainder‖ :=
        norm_sub_le _ _
  linarith

/-- Reverse-triangle coercivity instantiated with the scaled Spartan chord.

Inside the normalized range, adding a remainder of norm at most `error`
preserves the lower bound `2 |u| / π - error`.
-/
theorem quznorSpartan_scaledChord_profile_coercivity
    (u : ℝ) (N : ℕ) (hN : 0 < N)
    (remainder : ℂ) (error : ℝ)
    (hu : |u| ≤ Real.pi * (N : ℝ))
    (hremainder : ‖remainder‖ ≤ error) :
    2 * |u| / Real.pi - error ≤
      ‖(N : ℝ) •
          (Complex.exp
              (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1) +
        remainder‖ := by
  have hchord :=
    quznorSpartan_scaledChord_uniformLowerBound u N hN hu
  have hmain :
      2 * |u| / Real.pi ≤
        ‖(N : ℝ) •
            (Complex.exp
                (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1)‖ := by
    simpa [
      norm_smul,
      Real.norm_eq_abs,
      abs_of_nonneg (show 0 ≤ (N : ℝ) from Nat.cast_nonneg N)
    ] using hchord
  exact
    quznorSpartan_reverseTriangle_coercivity
      ((N : ℝ) •
        (Complex.exp
            (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1))
      remainder
      (2 * |u| / Real.pi)
      error
      hmain
      hremainder

/-- Strict scaled-chord profile coercivity from a quantitative remainder gap.

If the remainder norm is bounded by `error` and that error is strictly smaller
than the scaled chord lower bound, then the perturbed profile has positive norm.
-/
theorem quznorSpartan_scaledChord_profile_pos
    (u : ℝ) (N : ℕ) (hN : 0 < N)
    (remainder : ℂ) (error : ℝ)
    (hu : |u| ≤ Real.pi * (N : ℝ))
    (hremainder : ‖remainder‖ ≤ error)
    (herror : error < 2 * |u| / Real.pi) :
    0 <
      ‖(N : ℝ) •
          (Complex.exp
              (Complex.I * (((u / (N : ℝ)) : ℝ) : ℂ)) - 1) +
        remainder‖ := by
  have hcoercivity :=
    quznorSpartan_scaledChord_profile_coercivity
      u N hN remainder error hu hremainder
  linarith

/-- The complex-coordinate form of the documented Spartan profile.

The first summand is the fundamental circular mode with coefficient
`sqrt ((N² M - E)/(N² - 1))`; the second is the frequency-`N` mode with
coefficient `sqrt ((E - M)/(N² - 1))`.
-/
noncomputable def quznorSpartanComplexProfile
    (M E : ℝ) (N : ℕ) (θ : ℝ) : ℂ :=
  ((Real.sqrt
      ((((N : ℝ) ^ 2) * M - E) /
        (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
      Complex.exp (Complex.I * (θ : ℂ)) +
    ((Real.sqrt
      ((E - M) /
        (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
      Complex.exp
        (Complex.I * ((((N : ℝ) * θ : ℝ)) : ℂ))



/--
Weak typed bridge from the native Spartan profile to sampled scalar
curvature.

The bridge asserts only that sampled curvature is `N` times the value of
an arbitrary real-valued observable applied to the native profile. It
does not assert positivity, convergence, or a geometric curvature law.
-/
structure QuznorSpartanProfileCurvatureBridge (M E : ℝ) where
  normalizedCurvatureFromProfile : ℕ → (ℝ → ℂ) → ℝ
  scalarCurvatureAtSample : ℕ → ℝ
  scalarCurvatureAtSample_eq :
    ∀ N : ℕ,
      scalarCurvatureAtSample N =
        (N : ℝ) *
          normalizedCurvatureFromProfile N
            (quznorSpartanComplexProfile M E N)


/--
Exact normalized-curvature identity supplied by the typed bridge.

The restriction `0 < N` is only needed to cancel the normalization
factor. No sign condition on the resulting normalized curvature is used.
-/
theorem quznorSpartanProfileCurvatureBridge_normalized_identity
    {M E : ℝ}
    (bridge : QuznorSpartanProfileCurvatureBridge M E)
    (N : ℕ) (hN : 0 < N) :
    bridge.scalarCurvatureAtSample N / (N : ℝ) =
      bridge.normalizedCurvatureFromProfile N
        (quznorSpartanComplexProfile M E N) := by
  rw [bridge.scalarCurvatureAtSample_eq]
  have hN0 : (N : ℝ) ≠ 0 := by
    exact_mod_cast hN.ne'
  apply (div_eq_iff hN0).2
  ring


/--
A continuity-bearing observable interface linking the `N`-indexed bridge
observable to one real-valued functional of the complete profile.

Continuity is stated only at the fixed circular profile and directly in
the uniform norm needed by the compiled profile-convergence theorem.
No positivity or geometric-curvature interpretation is included.
-/
structure QuznorSpartanContinuousProfileCurvatureObservable
    {M E : ℝ}
    (bridge : QuznorSpartanProfileCurvatureBridge M E) where
  value : (ℝ → ℂ) → ℝ
  limitValue : ℝ
  bridge_value_eq :
    ∀ N : ℕ, ∀ profile : ℝ → ℂ,
      bridge.normalizedCurvatureFromProfile N profile =
        value profile
  continuousAtFixedCircle :
    ∀ ε > 0, ∃ δ > 0, ∀ profile : ℝ → ℂ,
      (∀ θ : ℝ,
        ‖profile θ -
          ((Real.sqrt M : ℝ) : ℂ) *
            Complex.exp (Complex.I * (θ : ℂ))‖ < δ) →
      |value profile - limitValue| < ε

/-- Exact error identity for the squared Spartan fundamental coefficient. -/
theorem quznorSpartan_fundamentalCoefficientSq_error_identity
    (M E : ℝ) (N : ℕ) (hN : 2 ≤ N) :
    ((((N : ℝ) ^ 2) * M - E) / (((N : ℝ) ^ 2) - 1)) - M =
      (M - E) / (((N : ℝ) ^ 2) - 1) := by
  have hNreal : (2 : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast hN
  have hdenpos : 0 < ((N : ℝ) ^ 2) - 1 := by
    nlinarith [sq_nonneg ((N : ℝ) - 2)]
  field_simp [ne_of_gt hdenpos]
  all_goals ring


/-- The squared Spartan fundamental coefficient converges to `M`. -/
theorem quznorSpartan_fundamentalCoefficientSq_tendsto
    (M E : ℝ) :
    Tendsto
      (fun N : ℕ =>
        (((N : ℝ) ^ 2) * M - E) / (((N : ℝ) ^ 2) - 1))
      atTop
      (nhds M) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨K, hK⟩ := exists_nat_gt (|M - E| / ε + 2)
  refine ⟨max 2 K, ?_⟩
  intro N hN
  have hNtwo : 2 ≤ N :=
    le_trans (le_max_left 2 K) hN
  have hKN : K ≤ N :=
    le_trans (le_max_right 2 K) hN
  have hNreal : (2 : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast hNtwo
  have hKNreal : (K : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast hKN
  have hdenpos : 0 < ((N : ℝ) ^ 2) - 1 := by
    nlinarith [sq_nonneg ((N : ℝ) - 2)]
  have hden_ge_N :
      (N : ℝ) ≤ ((N : ℝ) ^ 2) - 1 := by
    nlinarith [sq_nonneg ((N : ℝ) - 2)]
  have hratio_lt_N :
      |M - E| / ε < (N : ℝ) := by
    linarith
  have hratio_lt_den :
      |M - E| / ε < ((N : ℝ) ^ 2) - 1 :=
    lt_of_lt_of_le hratio_lt_N hden_ge_N
  have hnum_lt :
      |M - E| < ε * (((N : ℝ) ^ 2) - 1) := by
    simpa [mul_comm] using
      (div_lt_iff₀ hε).1 hratio_lt_den
  rw [
    Real.dist_eq,
    quznorSpartan_fundamentalCoefficientSq_error_identity M E N hNtwo,
    abs_div,
    abs_of_pos hdenpos
  ]
  exact (div_lt_iff₀ hdenpos).2 hnum_lt


/-- The Spartan fundamental coefficient converges to `sqrt M`. -/
theorem quznorSpartan_fundamentalCoefficient_tendsto_sqrt
    (M E : ℝ) :
    Tendsto
      (fun N : ℕ =>
        Real.sqrt
          ((((N : ℝ) ^ 2) * M - E) /
            (((N : ℝ) ^ 2) - 1)))
      atTop
      (nhds (Real.sqrt M)) := by
  exact
    (quznorSpartan_fundamentalCoefficientSq_tendsto M E).sqrt

/-- Exact fundamental-mode plus high-frequency-mode decomposition.

The second summand is the repository-native Spartan profile remainder term.
-/
theorem quznorSpartanComplexProfile_fundamental_add_highMode
    (M E : ℝ) (N : ℕ) (θ : ℝ) :
    quznorSpartanComplexProfile M E N θ =
      ((Real.sqrt
          ((((N : ℝ) ^ 2) * M - E) /
            (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ)) +
        ((Real.sqrt
          ((E - M) /
            (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
          Complex.exp
            (Complex.I * ((((N : ℝ) * θ : ℝ)) : ℂ)) := by
  rfl

/-- The frequency-`N` remainder term in the native Spartan complex profile. -/
noncomputable def quznorSpartanHighModeRemainder
    (M E : ℝ) (N : ℕ) (θ : ℝ) : ℂ :=
  ((Real.sqrt
      ((E - M) /
        (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
    Complex.exp
      (Complex.I * ((((N : ℝ) * θ : ℝ)) : ℂ))

/-- The high-frequency Spartan remainder has constant norm in `θ`. -/
theorem quznorSpartanHighModeRemainder_norm
    (M E : ℝ) (N : ℕ) (θ : ℝ) :
    ‖quznorSpartanHighModeRemainder M E N θ‖ =
      Real.sqrt
        ((E - M) /
          (((N : ℝ) ^ 2) - 1)) := by
  simp [
    quznorSpartanHighModeRemainder,
    Complex.norm_exp,
    Real.sqrt_nonneg
  ]


/--
The formal frequency-scaled high-mode term expected from differentiating
the Spartan frequency-`N` mode once.

This is an algebraic term definition only; it does not assert that it is
the derivative of `quznorSpartanComplexProfile`.
-/
noncomputable def quznorSpartanFirstDerivativeTerm
    (M E : ℝ) (N : ℕ) (θ : ℝ) : ℂ :=
  (((N : ℝ) : ℂ) * Complex.I) *
    quznorSpartanHighModeRemainder M E N θ

/--
Exact norm identity for the formal Spartan first-derivative term.
-/
theorem quznorSpartanFirstDerivativeTerm_norm
    (M E : ℝ) (N : ℕ) (θ : ℝ) :
    ‖quznorSpartanFirstDerivativeTerm M E N θ‖ =
      (N : ℝ) *
        Real.sqrt
          ((E - M) / (((N : ℝ) ^ 2) - 1)) := by
  rw [
    quznorSpartanFirstDerivativeTerm,
    norm_mul,
    quznorSpartanHighModeRemainder_norm
  ]
  simp

/-- Explicit inverse-scale bound for the Spartan high-frequency remainder.

For `M ≤ E` and `N ≥ 2`, the exact remainder amplitude is bounded by
`sqrt (2 * (E - M)) / N`.
-/
theorem quznorSpartanHighModeRemainder_norm_le_inv
    (M E : ℝ) (N : ℕ) (θ : ℝ)
    (hEM : M ≤ E) (hN : 2 ≤ N) :
    ‖quznorSpartanHighModeRemainder M E N θ‖ ≤
      Real.sqrt (2 * (E - M)) / (N : ℝ) := by
  rw [quznorSpartanHighModeRemainder_norm]
  have ha : 0 ≤ E - M := sub_nonneg.mpr hEM
  have hNreal : (2 : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast hN
  have hNpos : 0 < (N : ℝ) := by
    linarith
  have hn2pos : 0 < (N : ℝ) ^ 2 := sq_pos_of_pos hNpos
  have hn2ge : 2 ≤ (N : ℝ) ^ 2 := by
    nlinarith
  have hdenpos : 0 < (N : ℝ) ^ 2 - 1 := by
    linarith
  have hfrac_nonneg :
      0 ≤ (E - M) / ((N : ℝ) ^ 2 - 1) :=
    div_nonneg ha (le_of_lt hdenpos)
  have htwice_nonneg : 0 ≤ 2 * (E - M) :=
    mul_nonneg (by norm_num) ha
  have hfrac_le :
      (E - M) / ((N : ℝ) ^ 2 - 1) ≤
        (2 * (E - M)) / (N : ℝ) ^ 2 := by
    apply (div_le_div_iff₀ hdenpos hn2pos).2
    have hproduct :
        0 ≤ (E - M) * ((N : ℝ) ^ 2 - 2) :=
      mul_nonneg ha (sub_nonneg.mpr hn2ge)
    nlinarith
  have hleft_sq :
      (Real.sqrt
          ((E - M) / ((N : ℝ) ^ 2 - 1))) ^ 2 =
        (E - M) / ((N : ℝ) ^ 2 - 1) :=
    Real.sq_sqrt hfrac_nonneg
  have hright_sq :
      (Real.sqrt (2 * (E - M)) / (N : ℝ)) ^ 2 =
        (2 * (E - M)) / (N : ℝ) ^ 2 := by
    rw [div_pow, Real.sq_sqrt htwice_nonneg]
  have hleft_nonneg :
      0 ≤ Real.sqrt
        ((E - M) / ((N : ℝ) ^ 2 - 1)) :=
    Real.sqrt_nonneg _
  have hright_nonneg :
      0 ≤ Real.sqrt (2 * (E - M)) / (N : ℝ) :=
    div_nonneg (Real.sqrt_nonneg _) (le_of_lt hNpos)
  by_contra hnot
  have hlt :
      Real.sqrt (2 * (E - M)) / (N : ℝ) <
        Real.sqrt
          ((E - M) / ((N : ℝ) ^ 2 - 1)) :=
    lt_of_not_ge hnot
  have hsum_pos :
      0 <
        Real.sqrt
            ((E - M) / ((N : ℝ) ^ 2 - 1)) +
          Real.sqrt (2 * (E - M)) / (N : ℝ) := by
    nlinarith
  have hproduct_pos :
      0 <
        (Real.sqrt
            ((E - M) / ((N : ℝ) ^ 2 - 1)) -
          Real.sqrt (2 * (E - M)) / (N : ℝ)) *
        (Real.sqrt
            ((E - M) / ((N : ℝ) ^ 2 - 1)) +
          Real.sqrt (2 * (E - M)) / (N : ℝ)) :=
    mul_pos (sub_pos.mpr hlt) hsum_pos
  nlinarith

/-- The Spartan high-frequency remainder converges uniformly in `θ` to zero. -/
theorem quznorSpartanHighModeRemainder_uniform_tendsto_zero
    (M E : ℝ) (hEM : M ≤ E) :
    ∀ ε > 0, ∃ N₀ : ℕ, ∀ N ≥ N₀, ∀ θ : ℝ,
      ‖quznorSpartanHighModeRemainder M E N θ‖ < ε := by
  intro ε hε
  obtain ⟨K, hK⟩ :=
    exists_nat_gt (Real.sqrt (2 * (E - M)) / ε)
  refine ⟨max 2 K, ?_⟩
  intro N hN θ
  have hNtwo : 2 ≤ N :=
    le_trans (le_max_left 2 K) hN
  have hKN : K ≤ N :=
    le_trans (le_max_right 2 K) hN
  have hbound :=
    quznorSpartanHighModeRemainder_norm_le_inv
      M E N θ hEM hNtwo
  have hNposNat : 0 < N :=
    lt_of_lt_of_le (by norm_num) hNtwo
  have hNpos : 0 < (N : ℝ) := by
    exact_mod_cast hNposNat
  have hKleN : (K : ℝ) ≤ (N : ℝ) := by
    exact_mod_cast hKN
  have hratio_lt_N :
      Real.sqrt (2 * (E - M)) / ε < (N : ℝ) :=
    lt_of_lt_of_le hK hKleN
  have hnum_lt :
      Real.sqrt (2 * (E - M)) < ε * (N : ℝ) := by
    simpa [mul_comm] using (div_lt_iff₀ hε).1 hratio_lt_N
  have hinv_lt :
      Real.sqrt (2 * (E - M)) / (N : ℝ) < ε :=
    (div_lt_iff₀ hNpos).2 hnum_lt
  exact lt_of_le_of_lt hbound hinv_lt

/-- The native Spartan profile converges uniformly to its fundamental mode.

The limiting comparison still carries the `N`-dependent fundamental
coefficient; only the high-frequency remainder is removed here.
-/
theorem quznorSpartanComplexProfile_uniform_tendsto_fundamental
    (M E : ℝ) (hEM : M ≤ E) :
    ∀ ε > 0, ∃ N₀ : ℕ, ∀ N ≥ N₀, ∀ θ : ℝ,
      ‖quznorSpartanComplexProfile M E N θ -
          ((Real.sqrt
              ((((N : ℝ) ^ 2) * M - E) /
                (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
            Complex.exp (Complex.I * (θ : ℂ))‖ < ε := by
  intro ε hε
  obtain ⟨N₀, hN₀⟩ :=
    quznorSpartanHighModeRemainder_uniform_tendsto_zero
      M E hEM ε hε
  refine ⟨N₀, ?_⟩
  intro N hN θ
  have hrem := hN₀ N hN θ
  rw [quznorSpartanComplexProfile_fundamental_add_highMode]
  simpa [quznorSpartanHighModeRemainder] using hrem

/-- The native Spartan profile converges uniformly to the fixed circular
profile with coefficient `sqrt M`. -/
theorem quznorSpartanComplexProfile_uniform_tendsto_fixedCircle
    (M E : ℝ) (hEM : M ≤ E) :
    ∀ ε > 0, ∃ N₀ : ℕ, ∀ N ≥ N₀, ∀ θ : ℝ,
      ‖quznorSpartanComplexProfile M E N θ -
        ((Real.sqrt M : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ))‖ < ε := by
  intro ε hε
  have hhalf : 0 < ε / 2 := by
    linarith
  obtain ⟨Nr, hNr⟩ :=
    quznorSpartanHighModeRemainder_uniform_tendsto_zero
      M E hEM (ε / 2) hhalf
  have hcoeff :=
    quznorSpartan_fundamentalCoefficient_tendsto_sqrt M E
  rw [Metric.tendsto_atTop] at hcoeff
  obtain ⟨Nc, hNc⟩ := hcoeff (ε / 2) hhalf
  refine ⟨max Nr Nc, ?_⟩
  intro N hN θ
  have hNrN : Nr ≤ N :=
    le_trans (le_max_left Nr Nc) hN
  have hNcN : Nc ≤ N :=
    le_trans (le_max_right Nr Nc) hN
  have hrem := hNr N hNrN θ
  have hcoeffN := hNc N hNcN
  have hfund :
      ‖((Real.sqrt
              ((((N : ℝ) ^ 2) * M - E) /
                (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
            Complex.exp (Complex.I * (θ : ℂ)) -
          ((Real.sqrt M : ℝ) : ℂ) *
            Complex.exp (Complex.I * (θ : ℂ))‖ <
        ε / 2 := by
    rw [← sub_mul, norm_mul]
    have hexp :
        ‖Complex.exp (Complex.I * (θ : ℂ))‖ = 1 := by
      rw [Complex.norm_exp]
      simp
    rw [hexp, mul_one]
    have hcast :
        (((Real.sqrt
              ((((N : ℝ) ^ 2) * M - E) /
                (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) -
            ((Real.sqrt M : ℝ) : ℂ)) =
          ((Real.sqrt
              ((((N : ℝ) ^ 2) * M - E) /
                (((N : ℝ) ^ 2) - 1)) -
            Real.sqrt M : ℝ) : ℂ) := by
      norm_num
    simpa only [
      hcast,
      Complex.norm_real,
      Real.norm_eq_abs,
      Real.dist_eq
    ] using hcoeffN
  rw [quznorSpartanComplexProfile_fundamental_add_highMode]
  change
    ‖((Real.sqrt
            ((((N : ℝ) ^ 2) * M - E) /
              (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ)) +
        quznorSpartanHighModeRemainder M E N θ -
        ((Real.sqrt M : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ))‖ < ε
  calc
    ‖((Real.sqrt
            ((((N : ℝ) ^ 2) * M - E) /
              (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ)) +
        quznorSpartanHighModeRemainder M E N θ -
        ((Real.sqrt M : ℝ) : ℂ) *
          Complex.exp (Complex.I * (θ : ℂ))‖ =
        ‖(((Real.sqrt
                ((((N : ℝ) ^ 2) * M - E) /
                  (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
              Complex.exp (Complex.I * (θ : ℂ)) -
            ((Real.sqrt M : ℝ) : ℂ) *
              Complex.exp (Complex.I * (θ : ℂ))) +
          quznorSpartanHighModeRemainder M E N θ‖ := by
            congr 1
            ring
    _ ≤
        ‖((Real.sqrt
                ((((N : ℝ) ^ 2) * M - E) /
                  (((N : ℝ) ^ 2) - 1)) : ℝ) : ℂ) *
              Complex.exp (Complex.I * (θ : ℂ)) -
            ((Real.sqrt M : ℝ) : ℂ) *
              Complex.exp (Complex.I * (θ : ℂ))‖ +
          ‖quznorSpartanHighModeRemainder M E N θ‖ :=
      norm_add_le _ _
    _ < ε / 2 + ε / 2 :=
      add_lt_add hfund hrem
    _ = ε := by
      ring


/--
Uniform convergence of the native Spartan profile transfers through any
observable satisfying the continuity interface.

The theorem contains no positivity conclusion.
-/
theorem quznorSpartanContinuousProfileCurvatureObservable_tendsto
    {M E : ℝ}
    (hEM : M ≤ E)
    (bridge : QuznorSpartanProfileCurvatureBridge M E)
    (observable :
      QuznorSpartanContinuousProfileCurvatureObservable bridge) :
    Tendsto
      (fun N : ℕ =>
        bridge.normalizedCurvatureFromProfile N
          (quznorSpartanComplexProfile M E N))
      atTop
      (nhds observable.limitValue) := by
  rw [Metric.tendsto_atTop]
  intro ε hε
  obtain ⟨δ, hδ, hcontinuous⟩ :=
    observable.continuousAtFixedCircle ε hε
  obtain ⟨N₀, hprofile⟩ :=
    quznorSpartanComplexProfile_uniform_tendsto_fixedCircle
      M E hEM δ hδ
  refine ⟨N₀, ?_⟩
  intro N hN
  rw [Real.dist_eq]
  rw [
    observable.bridge_value_eq N
      (quznorSpartanComplexProfile M E N)
  ]
  exact
    hcontinuous
      (quznorSpartanComplexProfile M E N)
      (hprofile N hN)


/--
The exact bridge identity transfers observable convergence to normalized
sampled-curvature convergence.

Positivity of the limiting value remains a separate hypothesis.
-/
theorem quznorSpartanProfileCurvatureBridge_normalizedSample_tendsto
    {M E : ℝ}
    (hEM : M ≤ E)
    (bridge : QuznorSpartanProfileCurvatureBridge M E)
    (observable :
      QuznorSpartanContinuousProfileCurvatureObservable bridge) :
    Tendsto
      (fun N : ℕ =>
        bridge.scalarCurvatureAtSample N / (N : ℝ))
      atTop
      (nhds observable.limitValue) := by
  have hobservable :=
    quznorSpartanContinuousProfileCurvatureObservable_tendsto
      hEM bridge observable
  rw [Metric.tendsto_atTop] at hobservable ⊢
  intro ε hε
  obtain ⟨N₀, hN₀⟩ := hobservable ε hε
  refine ⟨max 1 N₀, ?_⟩
  intro N hN
  have hOne : 1 ≤ N :=
    le_trans (le_max_left 1 N₀) hN
  have hNpos : 0 < N :=
    lt_of_lt_of_le Nat.zero_lt_one hOne
  have hN₀N : N₀ ≤ N :=
    le_trans (le_max_right 1 N₀) hN
  rw [
    quznorSpartanProfileCurvatureBridge_normalized_identity
      bridge N hNpos
  ]
  exact hN₀ N hN₀N


/--
Separate positivity hypothesis for the limiting normalized curvature.

This proposition is not derived from profile convergence or continuity.
-/
def QuznorSpartanProfileCurvatureLimitPositive
    {M E : ℝ}
    {bridge : QuznorSpartanProfileCurvatureBridge M E}
    (observable :
      QuznorSpartanContinuousProfileCurvatureObservable bridge) :
    Prop :=
  0 < observable.limitValue


/--
Weakest typed identification of the bridge's sampled-curvature sequence
with a supplied geometric scalar-curvature sequence.

This interface supplies only an exact pointwise identification. It does
not construct geometry, prove a curvature formula, establish convergence,
or assert positivity.
-/
structure QuznorSpartanGeometricCurvatureIdentification
    {M E : ℝ}
    (bridge : QuznorSpartanProfileCurvatureBridge M E) where
  geometricScalarCurvatureAtSample : ℕ → ℝ
  geometricScalarCurvatureAtSample_eq :
    ∀ N : ℕ,
      geometricScalarCurvatureAtSample N =
        bridge.scalarCurvatureAtSample N


/--
Transport the compiled normalized profile-observable convergence into the
existing conditional curvature certificate.

Strict positivity remains an explicit input. The geometric identification
remains supplied data rather than a derived curvature law.
-/
noncomputable def
    quznorSpartanConditionalCurvatureBlowupData_of_geometricIdentification
    {M E : ℝ}
    (hEM : M ≤ E)
    (bridge : QuznorSpartanProfileCurvatureBridge M E)
    (observable :
      QuznorSpartanContinuousProfileCurvatureObservable bridge)
    (identification :
      QuznorSpartanGeometricCurvatureIdentification bridge)
    (hpositive :
      QuznorSpartanProfileCurvatureLimitPositive observable)
    (fixedFiberData : QuznorSpartanFixedFiberData)
    (scalarCurvatureSup : ℕ → ℝ)
    (sample_le_sup :
      ∀ N : ℕ,
        identification.geometricScalarCurvatureAtSample N ≤
          scalarCurvatureSup N) :
    QuznorSpartanConditionalCurvatureBlowupData where
  fiberData := fun _ => fixedFiberData
  fixedFiberData := fixedFiberData
  fiberData_fixed := by
    intro N
    rfl
  scalarCurvatureAtSample :=
    identification.geometricScalarCurvatureAtSample
  scalarCurvatureSup := scalarCurvatureSup
  sample_le_sup := sample_le_sup
  c0 := observable.limitValue
  c0_pos := by
    simpa [QuznorSpartanProfileCurvatureLimitPositive] using hpositive
  normalizedSampleTendsto := by
    have hnormalized :=
      quznorSpartanProfileCurvatureBridge_normalizedSample_tendsto
        hEM bridge observable
    simpa only [
      identification.geometricScalarCurvatureAtSample_eq
    ] using hnormalized

/--
The existing conditional Spartan curvature-blowup theorem applies after
supplying geometric identification, supremum domination, and explicit
positivity of the normalized-curvature limit.
-/
theorem
    quznorSpartanConditionalCurvatureBlowup_of_geometricIdentification
    {M E : ℝ}
    (hEM : M ≤ E)
    (bridge : QuznorSpartanProfileCurvatureBridge M E)
    (observable :
      QuznorSpartanContinuousProfileCurvatureObservable bridge)
    (identification :
      QuznorSpartanGeometricCurvatureIdentification bridge)
    (hpositive :
      QuznorSpartanProfileCurvatureLimitPositive observable)
    (fixedFiberData : QuznorSpartanFixedFiberData)
    (scalarCurvatureSup : ℕ → ℝ)
    (sample_le_sup :
      ∀ N : ℕ,
        identification.geometricScalarCurvatureAtSample N ≤
          scalarCurvatureSup N) :
    (∀ _ : ℕ, fixedFiberData = fixedFiberData) ∧
      Tendsto scalarCurvatureSup atTop atTop := by
  let data :=
    quznorSpartanConditionalCurvatureBlowupData_of_geometricIdentification
      hEM bridge observable identification hpositive fixedFiberData
        scalarCurvatureSup sample_le_sup
  have hcertificate :=
    quznorSpartanConditionalCurvatureBlowup data
  refine ⟨?_, ?_⟩
  · intro _
    rfl
  · exact hcertificate.2


end Chronos.Frontier
