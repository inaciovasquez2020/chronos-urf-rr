import AngularDensityAssembly
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

noncomputable section

private def spatialBall : Set Space :=
  {v | ‖v‖ < 1}

private theorem spatialBall_measurable :
    MeasurableSet spatialBall := by
  exact
    (isOpen_lt
      (f := fun v : Space => ‖v‖)
      (g := fun _ : Space => 1)
      continuous_norm continuous_const).measurableSet

private theorem packed_norm
    (x : ℝ) (v : Fin 2 → ℝ) :
    ‖pack x v‖ =
      Real.sqrt (x^2+transverseSq v) := by
  have h :
      ‖pack x v‖^2 =
        x^2+transverseSq v := by
    simp [pack,transverseSq,
      EuclideanSpace.real_norm_sq_eq,
      Fin.sum_univ_succ] <;> ring

  rw [← h,Real.sqrt_sq (norm_nonneg _)]

private theorem packed_coordinate
    (x : ℝ) (v : Fin 2 → ℝ) :
    (pack x v) 0 = x := by
  simp [pack]

private theorem transverse_null :
    (volume : Measure (Fin 2 → ℝ))
      {v | transverseSq v ≤ 0} = 0 := by
  unfold transverseSq
  rw [transverse_disk_mass]
  simp

private theorem transverse_positive_ae :
    ∀ᵐ v : Fin 2 → ℝ ∂volume,
      0 < transverseSq v := by

  have h :=
    measure_eq_zero_iff_ae_notMem.mp
      transverse_null

  filter_upwards [h] with v hv

  change ¬ transverseSq v ≤ 0 at hv
  exact lt_of_not_ge hv

private def axialWeight
    (F : ℝ × ℝ → ℝ≥0∞)
    (v : Space) : ℝ≥0∞ :=
  spatialBall.indicator
    (fun w => F (‖w‖,w 0/‖w‖)) v

private theorem axialWeight_measurable
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    Measurable (axialWeight F) := by
  unfold axialWeight
  apply Measurable.indicator _
    spatialBall_measurable
  fun_prop

private theorem packed_weight_slice
    (F : ℝ × ℝ → ℝ≥0∞)
    (x : ℝ) :
    (∫⁻ v : Fin 2 → ℝ,
      axialWeight F (pack x v)) =
      (Ioo (-1 : ℝ) 1).indicator
        (fun a =>
          ∫⁻ v in
            {v : Fin 2 → ℝ |
              transverseSq v ∈
                Ioo 0 (1-a^2)},
            F
              (Real.sqrt (a^2+transverseSq v),
              a/Real.sqrt
                (a^2+transverseSq v))) x := by

  by_cases hx : x ∈ Ioo (-1 : ℝ) 1

  · rw [Set.indicator_of_mem hx]

    let S : Set (Fin 2 → ℝ) :=
      {v | transverseSq v ∈
        Ioo 0 (1-x^2)}

    have hS : MeasurableSet S := by
      have hm : Measurable transverseSq := by
        unfold transverseSq
        fun_prop
      exact hm measurableSet_Ioo

    change
      (∫⁻ v : Fin 2 → ℝ,
        axialWeight F (pack x v)) =
        ∫⁻ v in S,
          F
            (Real.sqrt (x^2+transverseSq v),
            x/Real.sqrt
              (x^2+transverseSq v))

    rw [← lintegral_indicator hS]

    apply lintegral_congr_ae

    filter_upwards [transverse_positive_ae]
      with v hv

    have hn : 0 ≤ x^2+transverseSq v :=
      add_nonneg (sq_nonneg x) hv.le

    have hs :
        (Real.sqrt
          (x^2+transverseSq v))^2 =
          x^2+transverseSq v :=
      Real.sq_sqrt hn

    have hlt :
        ‖pack x v‖ < 1 ↔
          transverseSq v < 1-x^2 := by

      rw [packed_norm]

      constructor

      · intro h
        have hh :=
          (sq_lt_sq₀
            (Real.sqrt_nonneg _) zero_le_one).mpr h
        rw [hs] at hh
        linarith

      · intro h
        apply (sq_lt_sq₀
          (Real.sqrt_nonneg _) zero_le_one).mp
        rw [hs]
        linarith

    have he : pack x v ∈ spatialBall ↔ v ∈ S := by
      change ‖pack x v‖ < 1 ↔
        0 < transverseSq v ∧
          transverseSq v < 1-x^2
      rw [hlt]
      simp [hv]

    by_cases h : v ∈ S

    · rw [Set.indicator_of_mem h]
      unfold axialWeight
      rw [Set.indicator_of_mem (he.mpr h),
        packed_norm,packed_coordinate]

    · rw [Set.indicator_of_notMem h]
      unfold axialWeight
      exact Set.indicator_of_notMem
        (fun hp => h (he.mp hp)) _

  · rw [Set.indicator_of_notMem hx]

    calc
      _ = ∫⁻ _ : Fin 2 → ℝ, (0 : ℝ≥0∞) := by
        apply lintegral_congr
        intro v

        have hv : 0 ≤ transverseSq v := by
          unfold transverseSq
          positivity

        have hn : pack x v ∉ spatialBall := by
          intro hp

          change ‖pack x v‖ < 1 at hp
          rw [packed_norm] at hp

          have hs :=
            (sq_lt_sq₀
              (Real.sqrt_nonneg _) zero_le_one).mpr hp

          rw [Real.sq_sqrt
            (add_nonneg (sq_nonneg x) hv)] at hs

          apply hx
          apply abs_lt.mp
          apply (sq_lt_sq₀
            (abs_nonneg x) zero_le_one).mp
          rw [sq_abs]
          linarith

        unfold axialWeight
        exact Set.indicator_of_notMem hn _

      _ = 0 := lintegral_zero

theorem physical_axial_angular_integral
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ v in spatialBall,
      F (‖v‖,v 0/‖v‖)) =
      ENNReal.ofReal Real.pi *
        ∫⁻ r in Ioo (0 : ℝ) 1,
          ENNReal.ofReal (2*r^2) *
            ∫⁻ c in Ioo (-1 : ℝ) 1,
              F (r,c) := by

  have hpack : MeasurePreserving
      (fun p : ℝ × (Fin 2 → ℝ) =>
        pack p.1 p.2) :=
    pack_measurePreserving

  have hM := axialWeight_measurable F hF

  have hchange :
      (∫⁻ v, axialWeight F v) =
        ∫⁻ p : ℝ × (Fin 2 → ℝ),
          axialWeight F (pack p.1 p.2) := by

    have h :=
      lintegral_map
        (μ := (volume : Measure (ℝ × (Fin 2 → ℝ))))
        hM hpack.measurable

    rw [hpack.map_eq] at h

    exact h

  calc
    _ = ∫⁻ v, axialWeight F v := by
      unfold axialWeight
      rw [lintegral_indicator spatialBall_measurable]

    _ = ∫⁻ p : ℝ × (Fin 2 → ℝ),
        axialWeight F (pack p.1 p.2) :=
      hchange

    _ = ∫⁻ x : ℝ,
        ∫⁻ v : Fin 2 → ℝ,
          axialWeight F (pack x v) := by

      rw [Measure.volume_eq_prod]

      exact lintegral_prod _
        ((hM.comp hpack.measurable).aemeasurable)

    _ = ∫⁻ x in Ioo (-1 : ℝ) 1,
        ∫⁻ v in
          {v : Fin 2 → ℝ |
            transverseSq v ∈ Ioo 0 (1-x^2)},
          F
            (Real.sqrt (x^2+transverseSq v),
            x/Real.sqrt
              (x^2+transverseSq v)) := by

      rw [← lintegral_indicator measurableSet_Ioo]

      apply lintegral_congr
      intro x

      exact packed_weight_slice F x

    _ = _ := angular_ball_integral F hF

theorem physical_direction_angular_integral
    (e : Space) (he : ‖e‖ = 1)
    (F : ℝ × ℝ → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ v in spatialBall,
      F (‖v‖,⟪e,v⟫_ℝ/‖v‖)) =
      ENNReal.ofReal Real.pi *
        ∫⁻ r in Ioo (0 : ℝ) 1,
          ENNReal.ofReal (2*r^2) *
            ∫⁻ c in Ioo (-1 : ℝ) 1,
              F (r,c) := by

  have ha : ‖axis 1‖ = 1 := by
    simp [axis,PiLp.norm_single]

  let J : Space ≃ₗᵢ[ℝ] Space :=
    Submodule.reflection (ℝ ∙ (e-axis 1))ᗮ

  have hJ : J e = axis 1 :=
    Submodule.reflection_sub (he.trans ha.symm)

  have hinner (v : Space) :
      ⟪e,v⟫_ℝ = (J v) 0 := by

    calc
      _ = ⟪J e,J v⟫_ℝ :=
        (J.inner_map_map e v).symm
      _ = _ := by
        rw [hJ]
        simpa [axis] using
          (EuclideanSpace.inner_single_left
            (𝕜 := ℝ)
            (0 : Fin 3) (1 : ℝ) (J v))

  have hpoint (v : Space) :
      spatialBall.indicator
        (fun w =>
          F (‖w‖,⟪e,w⟫_ℝ/‖w‖)) v =
        axialWeight F (J v) := by

    have hm :
        J v ∈ spatialBall ↔
          v ∈ spatialBall := by
      change ‖J v‖ < 1 ↔ ‖v‖ < 1
      rw [J.norm_map]

    unfold axialWeight

    by_cases hv : v ∈ spatialBall

    · rw [Set.indicator_of_mem hv,
        Set.indicator_of_mem (hm.mpr hv),
        J.norm_map,hinner]

    · rw [Set.indicator_of_notMem hv,
        Set.indicator_of_notMem
          (fun h => hv (hm.mp h))]

  have hchange :
      (∫⁻ v, axialWeight F (J v)) =
        ∫⁻ v, axialWeight F v := by

    have h :=
      lintegral_map
        (μ := (volume : Measure Space))
        (axialWeight_measurable F hF)
        J.continuous.measurable

    rw [J.measurePreserving.map_eq] at h

    exact h.symm

  calc
    _ = ∫⁻ v,
        spatialBall.indicator
          (fun w =>
            F (‖w‖,⟪e,w⟫_ℝ/‖w‖)) v := by
      rw [lintegral_indicator spatialBall_measurable]

    _ = ∫⁻ v, axialWeight F (J v) :=
      lintegral_congr hpoint

    _ = ∫⁻ v, axialWeight F v :=
      hchange

    _ = ∫⁻ v in spatialBall,
        F (‖v‖,v 0/‖v‖) := by
      unfold axialWeight
      rw [lintegral_indicator spatialBall_measurable]

    _ = _ := physical_axial_angular_integral F hF

#print axioms physical_axial_angular_integral
#print axioms physical_direction_angular_integral

end

end Chronos.FourEvent
