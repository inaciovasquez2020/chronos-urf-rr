import AngularMeasure

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

private theorem sq_meas :
    Measurable transverseSq := by
  unfold transverseSq
  fun_prop

private theorem transverse_restricted_integral
    (b : ℝ) (hb : b ≤ 1)
    (f : ℝ → ℝ≥0∞) (hf : Measurable f) :
    (∫⁻ v in {v : Fin 2 → ℝ |
      transverseSq v ∈ Ioo 0 b},
      f (transverseSq v)) =
        ENNReal.ofReal Real.pi *
          ∫⁻ u in Ioo 0 b, f u := by

  let D : Set (Fin 2 → ℝ) :=
    {v | transverseSq v ≤ 1}

  let S : Set ℝ := Ioo 0 b
  let A := transverseSq ⁻¹' S

  have hS : MeasurableSet S :=
    measurableSet_Ioo

  have hA : MeasurableSet A :=
    sq_meas hS

  have hAD : A ⊆ D := by
    intro v hv
    exact hv.2.le.trans hb

  have hSI : S ⊆ Ioc (0 : ℝ) 1 := by
    intro u hu
    exact ⟨hu.1,hu.2.le.trans hb⟩

  have hm :
      ((volume : Measure (Fin 2 → ℝ)).restrict
        D).map transverseSq =
        ENNReal.ofReal Real.pi •
          volume.restrict (Ioc (0 : ℝ) 1) :=
    transverse_square_pushforward

  change
    (∫⁻ v in A, f (transverseSq v)) = _

  calc
    _ = ∫⁻ v,
        A.indicator
          (fun w => f (transverseSq w)) v
          ∂volume.restrict D := by
      rw [lintegral_indicator hA,
        Measure.restrict_restrict_of_subset hAD]
    _ = ∫⁻ v,
        S.indicator f (transverseSq v)
          ∂volume.restrict D := by
      apply lintegral_congr
      intro v
      by_cases hv : transverseSq v ∈ S
      · have h : v ∈ A := hv
        simp [Set.indicator_of_mem,h,hv]
      · have h : v ∉ A := hv
        simp [Set.indicator_of_notMem,h,hv]
    _ = ∫⁻ u, S.indicator f u
        ∂(Measure.map transverseSq
          (Measure.restrict
            (volume : Measure (Fin 2 → ℝ)) D)) := by
      exact (lintegral_map
        (hf.indicator hS) sq_meas).symm
    _ = _ := by
      rw [hm,lintegral_smul_measure,
        smul_eq_mul,
        lintegral_indicator hS,
        Measure.restrict_restrict_of_subset hSI]

private theorem radial_slice
    (x : ℝ) (hx : |x| < 1)
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ v in {v : Fin 2 → ℝ |
      transverseSq v ∈ Ioo 0 (1-x^2)},
      F (Real.sqrt (x^2+transverseSq v),
        x / Real.sqrt (x^2+transverseSq v))) =
      ENNReal.ofReal Real.pi *
        ∫⁻ r in Ioo |x| 1,
          ENNReal.ofReal (2*r) *
            F (r,x/r) := by

  let f : ℝ → ℝ≥0∞ :=
    fun u => F (Real.sqrt (x^2+u),
      x / Real.sqrt (x^2+u))

  have hf : Measurable f := by
    unfold f
    fun_prop

  change (∫⁻ v in {v : Fin 2 → ℝ |
    transverseSq v ∈ Ioo 0 (1-x^2)},
    f (transverseSq v)) = _

  rw [transverse_restricted_integral
    (1-x^2) (by nlinarith [sq_nonneg x]) f hf]

  rw [radial_square_substitution x hx f]

  congr 1
  apply setLIntegral_congr_fun measurableSet_Ioo

  intro r hr

  have hr0 : 0 ≤ r :=
    (abs_nonneg x).trans hr.1.le

  have hsq : x^2+(r^2-x^2) = r^2 := by
    ring

  simp only [f,hsq,Real.sqrt_sq hr0]

private noncomputable def radialAngleIntegrand
    (F : ℝ × ℝ → ℝ≥0∞)
    (p : ℝ × ℝ) : ℝ≥0∞ :=
  if |p.1| < p.2 ∧ p.2 < 1 then
    ENNReal.ofReal (2*p.2) *
      F (p.2,p.1/p.2)
  else 0

private theorem radialAngleIntegrand_measurable
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    Measurable (radialAngleIntegrand F) := by
  unfold radialAngleIntegrand

  have hS : MeasurableSet
      {p : ℝ × ℝ |
        |p.1| < p.2 ∧ p.2 < 1} := by
    exact
      (isOpen_lt
        (f := fun p : ℝ × ℝ => |p.1|)
        (g := fun p : ℝ × ℝ => p.2)
        (by fun_prop)
        (by fun_prop)).measurableSet.inter
      (isOpen_lt
        (f := fun p : ℝ × ℝ => p.2)
        (g := fun _ : ℝ × ℝ => 1)
        (by fun_prop)
        (by fun_prop)).measurableSet

  exact Measurable.ite hS
    (by fun_prop) measurable_const

private theorem integrate_x_first
    (F : ℝ × ℝ → ℝ≥0∞) :
    (∫⁻ x in Ioo (-1 : ℝ) 1,
      ∫⁻ r in Ioo |x| 1,
        ENNReal.ofReal (2*r)*F (r,x/r)) =
      ∫⁻ x : ℝ, ∫⁻ r : ℝ,
        radialAngleIntegrand F (x,r) := by

  rw [← lintegral_indicator measurableSet_Ioo]

  apply lintegral_congr
  intro x

  by_cases hx : x ∈ Ioo (-1 : ℝ) 1
  · rw [Set.indicator_of_mem hx,
      ← lintegral_indicator measurableSet_Ioo]

    apply lintegral_congr
    intro r

    by_cases hr : r ∈ Ioo |x| 1
    · simp [radialAngleIntegrand,
        Set.indicator_of_mem hr,hr.1,hr.2]
    · have hn : ¬ (|x| < r ∧ r < 1) := hr

      simp [radialAngleIntegrand,
        Set.indicator_of_notMem hr,hn]
  · rw [Set.indicator_of_notMem hx]

    symm
    calc
      _ = ∫⁻ _ : ℝ, (0 : ℝ≥0∞) := by
        apply lintegral_congr
        intro r
        have hn : ¬ (|x| < r ∧ r < 1) := by
          intro h
          have hh : |x| < 1 :=
            h.1.trans h.2
          exact hx (abs_lt.mp hh)
        simp [radialAngleIntegrand,hn]
      _ = 0 := lintegral_zero

private theorem integrate_r_first
    (F : ℝ × ℝ → ℝ≥0∞) :
    (∫⁻ r : ℝ, ∫⁻ x : ℝ,
      radialAngleIntegrand F (x,r)) =
      ∫⁻ r in Ioo (0 : ℝ) 1,
        ∫⁻ x in Ioo (-r) r,
          ENNReal.ofReal (2*r)*F (r,x/r) := by

  rw [← lintegral_indicator measurableSet_Ioo]

  apply lintegral_congr
  intro r

  by_cases hr : r ∈ Ioo (0 : ℝ) 1
  · rw [Set.indicator_of_mem hr,
      ← lintegral_indicator measurableSet_Ioo]

    apply lintegral_congr
    intro x

    by_cases hx : x ∈ Ioo (-r) r
    · have h : |x| < r :=
        abs_lt.mpr hx
      simp [radialAngleIntegrand,
        Set.indicator_of_mem hx,h,hr.2]
    · have hn : ¬ |x| < r := by
        intro h
        exact hx (abs_lt.mp h)

      simp [radialAngleIntegrand,
        Set.indicator_of_notMem hx,hn]
  · rw [Set.indicator_of_notMem hr]

    calc
      _ = ∫⁻ _ : ℝ, (0 : ℝ≥0∞) := by
        apply lintegral_congr
        intro x
        have hn : ¬ (|x| < r ∧ r < 1) := by
          intro h
          exact hr
            ⟨lt_of_le_of_lt (abs_nonneg x) h.1,
              h.2⟩
        simp [radialAngleIntegrand,hn]
      _ = 0 := lintegral_zero

theorem angular_ball_integral
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ x in Ioo (-1 : ℝ) 1,
      ∫⁻ v in {v : Fin 2 → ℝ |
        transverseSq v ∈ Ioo 0 (1-x^2)},
        F (Real.sqrt (x^2+transverseSq v),
          x / Real.sqrt (x^2+transverseSq v))) =
      ENNReal.ofReal Real.pi *
        ∫⁻ r in Ioo (0 : ℝ) 1,
          ENNReal.ofReal (2*r^2) *
            ∫⁻ c in Ioo (-1 : ℝ) 1,
              F (r,c) := by

  let G : ℝ → ℝ≥0∞ :=
    fun x => ∫⁻ r in Ioo |x| 1,
      ENNReal.ofReal (2*r)*F (r,x/r)

  have hG : Measurable G := by
    have hM := radialAngleIntegrand_measurable F hF

    have he :
        G = fun x => ∫⁻ r : ℝ,
          radialAngleIntegrand F (x,r) := by

      funext x
      unfold G

      rw [← lintegral_indicator measurableSet_Ioo]

      apply lintegral_congr
      intro r
      by_cases hr : r ∈ Ioo |x| 1
      · simp [radialAngleIntegrand,
          Set.indicator_of_mem hr,hr.1,hr.2]
      · have hn : ¬ (|x| < r ∧ r < 1) := hr
        simp [radialAngleIntegrand,
          Set.indicator_of_notMem hr,hn]

    rw [he]
    exact Measurable.lintegral_prod_right
      (f := fun x r => radialAngleIntegrand F (x,r))
      (show Measurable
        (Function.uncurry
          (fun x r => radialAngleIntegrand F (x,r)))
        from hM)

  calc
    _ = ∫⁻ x in Ioo (-1 : ℝ) 1,
        ENNReal.ofReal Real.pi * G x := by
      apply setLIntegral_congr_fun measurableSet_Ioo
      intro x hx
      exact radial_slice x
        (abs_lt.mpr hx) F hF

    _ = ENNReal.ofReal Real.pi *
        ∫⁻ x in Ioo (-1 : ℝ) 1, G x := by
      rw [lintegral_const_mul _ hG]

    _ = ENNReal.ofReal Real.pi *
        ∫⁻ r in Ioo (0 : ℝ) 1,
          ∫⁻ x in Ioo (-r) r,
            ENNReal.ofReal (2*r)*F (r,x/r) := by
      unfold G
      rw [integrate_x_first F]
      rw [lintegral_lintegral_swap
        (f := fun x r =>
          radialAngleIntegrand F (x,r))
        (Measurable.aemeasurable
          (radialAngleIntegrand_measurable F hF))]
      rw [integrate_r_first F]

    _ = _ := by
      congr 1
      apply setLIntegral_congr_fun measurableSet_Ioo
      intro r hr

      have hmeas :
          Measurable (fun x : ℝ =>
            F (r,x/r)) := by fun_prop

      dsimp only
      rw [lintegral_const_mul _ hmeas,
        axial_cosine_substitution r hr.1]

      have he :
          (∫⁻ c in Ioo (-1 : ℝ) 1,
            ENNReal.ofReal r *
              F (r,r*c/r)) =
          ENNReal.ofReal r *
            ∫⁻ c in Ioo (-1 : ℝ) 1,
              F (r,c) := by

        have hs :
            ∀ c : ℝ, r*c/r = c := by
          intro c
          field_simp [ne_of_gt hr.1]

        simp_rw [hs]

        exact lintegral_const_mul _
          (show Measurable
            (fun c : ℝ => F (r,c))
            by fun_prop)

      rw [he,← mul_assoc,
        ← ENNReal.ofReal_mul
          (show 0 ≤ 2*r from
            mul_nonneg (by norm_num) hr.1.le)]

      congr 2
      ring

#print axioms angular_ball_integral

end Chronos.FourEvent
