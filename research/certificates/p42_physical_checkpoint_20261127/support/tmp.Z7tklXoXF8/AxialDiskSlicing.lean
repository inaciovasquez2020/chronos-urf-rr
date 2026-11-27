import CommonFutureVolume
import Mathlib.MeasureTheory.Measure.Lebesgue.VolumeOfBalls

open Set MeasureTheory WithLp
open scoped ENNReal

namespace Chronos.FourEvent

noncomputable def pack
    (x : ℝ) (v : Fin 2 → ℝ) : Space :=
  toLp 2 (Fin.cons x v)

theorem pack_norm_sq
    (x c : ℝ) (v : Fin 2 → ℝ) :
    ‖pack x v - axis c‖^2 =
      (x-c)^2 +
        ‖(toLp 2 v : EuclideanSpace ℝ (Fin 2))‖^2 := by
  simp [pack, axis,
    EuclideanSpace.real_norm_sq_eq,
    PiLp.sub_apply, PiLp.single_apply,
    Fin.sum_univ_succ]

theorem pack_measurePreserving :
    MeasurePreserving
      (fun q : ℝ × (Fin 2 → ℝ) =>
        pack q.1 q.2) := by
  let e :=
    MeasurableEquiv.piFinSuccAbove
      (fun _ : Fin 3 => ℝ) 0
  have he : MeasurePreserving e :=
    volume_preserving_piFinSuccAbove
      (fun _ : Fin 3 => ℝ) 0
  have h :=
    (PiLp.volume_preserving_toLp (Fin 3)).comp
      (he.symm e)
  simpa [pack, e, Function.comp_def,
    MeasurableEquiv.piFinSuccAbove,
    Fin.insertNthEquiv_zero] using h

theorem transverse_disk_mass (K : ℝ) :
    (volume : Measure (Fin 2 → ℝ))
      {v | ‖(toLp 2 v :
        EuclideanSpace ℝ (Fin 2))‖^2 ≤ K} =
      ENNReal.ofReal (K * Real.pi) := by
  let D : Set (EuclideanSpace ℝ (Fin 2)) :=
    {v | ‖v‖^2 ≤ K}
  have hm : MeasurableSet D :=
    (isClosed_le (by fun_prop)
      (by fun_prop)).measurableSet
  have hpre :
      (volume : Measure (Fin 2 → ℝ))
        {v | ‖(toLp 2 v :
          EuclideanSpace ℝ (Fin 2))‖^2 ≤ K} =
        volume D :=
    (PiLp.volume_preserving_toLp (Fin 2)).measure_preimage
      hm.nullMeasurableSet
  rw [hpre]
  by_cases hk : 0 ≤ K
  · have hd :
        D = Metric.closedBall 0 (Real.sqrt K) := by
      ext v
      change ‖v‖^2 ≤ K ↔
        dist v 0 ≤ Real.sqrt K
      rw [dist_zero_right,
        ← sq_le_sq₀ (norm_nonneg v)
          (Real.sqrt_nonneg K),
        Real.sq_sqrt hk]
    rw [hd, EuclideanSpace.volume_closedBall_fin_two,
      ← ENNReal.ofReal_pow (Real.sqrt_nonneg K),
      Real.sq_sqrt hk,
      ← ENNReal.ofReal_mul hk]
  · have hd : D = ∅ := by
      apply Set.eq_empty_iff_forall_notMem.mpr
      intro v hv
      change ‖v‖^2 ≤ K at hv
      exact hk ((sq_nonneg ‖v‖).trans hv)
    rw [hd, measure_empty]
    exact (ENNReal.ofReal_eq_zero.mpr
      (mul_nonpos_of_nonpos_of_nonneg
        (le_of_not_ge hk) Real.pi_nonneg)).symm

noncomputable def sectionRadiusSq
    (a b T s x : ℝ) : ℝ :=
  min (s^2-(x+a)^2)
    (min (s^2-(x-a)^2)
      ((T-s)^2-(x-b)^2))

noncomputable def sectionArea
    (a b T s x : ℝ) : ℝ≥0∞ :=
  if 0 ≤ s ∧ s ≤ T then
    ENNReal.ofReal
      (sectionRadiusSq a b T s x * Real.pi)
  else 0

theorem axial_transverse_slice
    (a b T s x : ℝ) :
    (volume : Measure (Fin 2 → ℝ))
      {v | (s, pack x v) ∈ axialLens a b T} =
      sectionArea a b T s x := by
  unfold sectionArea
  by_cases hs : 0 ≤ s ∧ s ≤ T
  · rw [if_pos hs]
    have hf :
        {v : Fin 2 → ℝ |
          (s, pack x v) ∈ axialLens a b T} =
        {v | ‖(toLp 2 v :
          EuclideanSpace ℝ (Fin 2))‖^2 ≤
            sectionRadiusSq a b T s x} := by
      ext v
      change
        (‖pack x v - axis (-a)‖ ≤ s - 0 ∧
         ‖pack x v - axis a‖ ≤ s - 0 ∧
         ‖axis b - pack x v‖ ≤ T-s) ↔
        ‖(toLp 2 v :
          EuclideanSpace ℝ (Fin 2))‖^2 ≤
            sectionRadiusSq a b T s x
      simp only [sub_zero]
      rw [norm_sub_rev (axis b) (pack x v)]
      rw [← sq_le_sq₀
            (norm_nonneg (pack x v-axis (-a))) hs.1,
          ← sq_le_sq₀
            (norm_nonneg (pack x v-axis a)) hs.1,
          ← sq_le_sq₀
            (norm_nonneg (pack x v-axis b))
            (sub_nonneg.mpr hs.2)]
      rw [pack_norm_sq, pack_norm_sq, pack_norm_sq]
      simp only [sectionRadiusSq, le_min_iff]
      constructor
      · rintro ⟨h₁,h₂,h₃⟩
        exact ⟨by nlinarith, by linarith,
          by linarith⟩
      · rintro ⟨h₁,h₂,h₃⟩
        exact ⟨by nlinarith, by linarith,
          by linarith⟩
    rw [hf]
    exact transverse_disk_mass _
  · rw [if_neg hs]
    have hf :
        {v : Fin 2 → ℝ |
          (s, pack x v) ∈ axialLens a b T} = ∅ := by
      apply Set.eq_empty_iff_forall_notMem.mpr
      intro v hv
      change
        ‖pack x v-axis (-a)‖ ≤ s-0 ∧
        ‖pack x v-axis a‖ ≤ s-0 ∧
        ‖axis b-pack x v‖ ≤ T-s at hv
      exact hs ⟨by linarith [norm_nonneg
        (pack x v-axis (-a))],
        by linarith [norm_nonneg
          (axis b-pack x v)]⟩
    rw [hf, measure_empty]

#print axioms pack_norm_sq
#print axioms pack_measurePreserving
#print axioms transverse_disk_mass
#print axioms axial_transverse_slice

end Chronos.FourEvent
