import AxialDiskSlicing
import Mathlib.MeasureTheory.Function.JacobianOneDim

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

noncomputable section

def transverseSq (v : Fin 2 → ℝ) : ℝ :=
  ‖(WithLp.toLp 2 v :
    EuclideanSpace ℝ (Fin 2))‖^2

private theorem transverseSq_measurable :
    Measurable transverseSq := by
  unfold transverseSq
  fun_prop

private theorem transverseSq_nonneg
    (v : Fin 2 → ℝ) :
    0 ≤ transverseSq v := by
  unfold transverseSq
  positivity

private def disk : Set (Fin 2 → ℝ) :=
  {v | transverseSq v ≤ 1}

theorem transverse_square_pushforward :
    ((volume : Measure (Fin 2 → ℝ)).restrict
      disk).map transverseSq =
        ENNReal.ofReal Real.pi •
          (volume.restrict (Ioc (0 : ℝ) 1)) := by

  have hdisk :
      (volume : Measure (Fin 2 → ℝ)) disk =
        ENNReal.ofReal Real.pi := by
    unfold disk transverseSq
    simpa using transverse_disk_mass (1 : ℝ)

  letI : IsFiniteMeasure
      ((volume : Measure (Fin 2 → ℝ)).restrict disk) :=
    isFiniteMeasure_restrict.mpr
      (by rw [hdisk]; exact ENNReal.ofReal_ne_top)

  letI : IsFiniteMeasure
      (((volume : Measure (Fin 2 → ℝ)).restrict
        disk).map transverseSq) :=
    Measure.isFiniteMeasure_map _ _

  apply Measure.ext_of_Iic
  intro u

  rw [Measure.map_apply transverseSq_measurable
        measurableSet_Iic,
    Measure.restrict_apply
      (transverseSq_measurable measurableSet_Iic),
    Measure.smul_apply, smul_eq_mul,
    Measure.restrict_apply measurableSet_Iic]

  by_cases hu : 0 ≤ u
  · let b := min u 1

    have hb : 0 ≤ b :=
      le_min hu zero_le_one

    have hleft :
        transverseSq ⁻¹' Iic u ∩ disk =
          {v | transverseSq v ≤ b} := by
      ext v
      simp only [mem_inter_iff,
        mem_preimage,mem_Iic,disk,
        mem_setOf_eq,b,le_min_iff]

    have hright :
        Iic u ∩ Ioc (0 : ℝ) 1 =
          Ioc 0 b := by
      ext t
      simp only [mem_inter_iff,
        mem_Iic,mem_Ioc,b,le_min_iff]
      tauto

    rw [hleft,hright]

    change
      (volume : Measure (Fin 2 → ℝ))
        {v | ‖(WithLp.toLp 2 v :
          EuclideanSpace ℝ (Fin 2))‖^2 ≤ b} =
          ENNReal.ofReal Real.pi * volume (Ioc 0 b)

    rw [transverse_disk_mass,Real.volume_Ioc,
      sub_zero,
      ← ENNReal.ofReal_mul Real.pi_pos.le]

    congr 1
    ring

  · have hleft :
        transverseSq ⁻¹' Iic u ∩ disk = ∅ := by
      ext v
      simp only [mem_inter_iff,mem_preimage,
        mem_Iic,mem_empty_iff_false]
      constructor
      · intro hv
        exact hu
          ((transverseSq_nonneg v).trans hv.1)
      · intro h
        exact h.elim

    have hright :
        Iic u ∩ Ioc (0 : ℝ) 1 = ∅ := by
      ext t
      simp only [mem_inter_iff,
        mem_Iic,mem_Ioc,mem_empty_iff_false]
      constructor
      · intro ht
        exact hu (ht.2.1.le.trans ht.1)
      · intro h
        exact h.elim

    rw [hleft,hright]
    simp

theorem transverse_square_integral
    (f : ℝ → ℝ≥0∞)
    (hf : Measurable f) :
    (∫⁻ v in disk, f (transverseSq v)) =
      ENNReal.ofReal Real.pi *
        ∫⁻ u in Ioc (0 : ℝ) 1, f u := by
  rw [← lintegral_map hf transverseSq_measurable,
    transverse_square_pushforward,
    lintegral_smul_measure]
  simp only [smul_eq_mul]

theorem radial_square_substitution
    (x : ℝ) (hx : |x| < 1)
    (f : ℝ → ℝ≥0∞) :
    (∫⁻ u in Ioo 0 (1-x^2), f u) =
      ∫⁻ r in Ioo |x| 1,
        ENNReal.ofReal (2*r) *
          f (r^2-x^2) := by

  let g : ℝ → ℝ := fun r => r^2-x^2

  have himage :
      g '' Ioo |x| 1 =
        Ioo 0 (1-x^2) := by
    ext u
    constructor
    · rintro ⟨r,hr,rfl⟩
      have hr0 : 0 < r :=
        lt_of_le_of_lt (abs_nonneg x) hr.1

      have h1 :=
        (sq_lt_sq₀
          (abs_nonneg x) hr0.le).mpr hr.1

      have h2 :=
        (sq_lt_sq₀
          hr0.le zero_le_one).mpr hr.2

      rw [sq_abs] at h1
      change 0 < r^2-x^2 ∧
        r^2-x^2 < 1-x^2
      constructor <;> nlinarith

    · intro hu
      have hpos : 0 < u+x^2 := by
        nlinarith [hu.1,sq_nonneg x]

      let r := Real.sqrt (u+x^2)

      have hr0 : 0 < r :=
        Real.sqrt_pos.2 hpos

      have hr2 : r^2 = u+x^2 :=
        Real.sq_sqrt hpos.le

      have h1 : |x| < r := by
        apply (sq_lt_sq₀
          (abs_nonneg x) hr0.le).mp
        rw [sq_abs,hr2]
        linarith [hu.1]

      have h2 : r < 1 := by
        apply (sq_lt_sq₀
          hr0.le zero_le_one).mp
        rw [hr2]
        nlinarith [hu.2]

      refine ⟨r,⟨h1,h2⟩,?_⟩
      change r^2-x^2 = u
      linarith

  have hderiv :
      ∀ r ∈ Ioo |x| 1,
        HasDerivWithinAt g (2*r)
          (Ioo |x| 1) r := by
    intro r hr
    have hd : HasDerivAt g (2*r) r := by
      dsimp [g]
      convert
        (((hasDerivAt_id r).pow 2).sub_const
          (x^2)) using 1 <;> simp only [id_eq] <;> ring
    exact hd.hasDerivWithinAt

  have hmono : MonotoneOn g (Ioo |x| 1) := by
    intro a ha b hb hab
    have ha0 : 0 ≤ a :=
      (abs_nonneg x).trans ha.1.le
    have hb0 : 0 ≤ b :=
      (abs_nonneg x).trans hb.1.le
    have hsq :=
      (sq_le_sq₀ ha0 hb0).mpr hab
    dsimp [g]
    linarith

  rw [← himage]

  exact lintegral_image_eq_lintegral_deriv_mul_of_monotoneOn
    measurableSet_Ioo hderiv hmono f

theorem axial_cosine_substitution
    (r : ℝ) (hr : 0 < r)
    (f : ℝ → ℝ≥0∞) :
    (∫⁻ x in Ioo (-r) r, f x) =
      ∫⁻ c in Ioo (-1 : ℝ) 1,
        ENNReal.ofReal r * f (r*c) := by

  let g : ℝ → ℝ := fun c => r*c

  have himage :
      g '' Ioo (-1 : ℝ) 1 =
        Ioo (-r) r := by
    ext x
    constructor
    · rintro ⟨c,hc,rfl⟩
      change -r < r*c ∧ r*c < r

      have h1 :=
        mul_lt_mul_of_pos_left hc.1 hr

      have h2 :=
        mul_lt_mul_of_pos_left hc.2 hr

      constructor <;> linarith

    · intro hx

      refine ⟨x/r,⟨?_,?_⟩,?_⟩

      · apply (lt_div_iff₀ hr).mpr
        linarith [hx.1]

      · apply (div_lt_iff₀ hr).mpr
        linarith [hx.2]

      · dsimp [g]
        field_simp [ne_of_gt hr]

  have hderiv :
      ∀ c ∈ Ioo (-1 : ℝ) 1,
        HasDerivWithinAt g r
          (Ioo (-1 : ℝ) 1) c := by
    intro c hc
    have hd : HasDerivAt g r c := by
      simpa [g] using
        (hasDerivAt_id c).const_mul r
    exact hd.hasDerivWithinAt

  have hmono :
      MonotoneOn g (Ioo (-1 : ℝ) 1) := by
    intro a ha b hb hab
    exact mul_le_mul_of_nonneg_left hab hr.le

  rw [← himage]

  exact lintegral_image_eq_lintegral_deriv_mul_of_monotoneOn
    measurableSet_Ioo hderiv hmono f

#print axioms transverse_square_pushforward
#print axioms transverse_square_integral
#print axioms radial_square_substitution
#print axioms axial_cosine_substitution

end

end Chronos.FourEvent
