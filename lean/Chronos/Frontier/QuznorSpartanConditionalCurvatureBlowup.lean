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

end Chronos.Frontier
