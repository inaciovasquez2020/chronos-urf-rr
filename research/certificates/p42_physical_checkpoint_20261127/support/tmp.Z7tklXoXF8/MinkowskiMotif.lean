import Mathlib.Analysis.InnerProductSpace.EuclideanDist
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.OpenPos
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Tactic

open Set MeasureTheory
open scoped ENNReal

namespace Chronos.FourEvent

abbrev Event := ℝ × EuclideanSpace ℝ (Fin 3)

def Precedes (x y : Event) : Prop :=
  ‖y.2 - x.2‖ ≤ y.1 - x.1

def diamond : Set Event :=
  {x | ‖x.2‖ < x.1 ∧ ‖x.2‖ < 1 - x.1}

noncomputable def uniform : Measure Event :=
  ((volume : Measure Event) diamond)⁻¹ • volume.restrict diamond

def commonFuture (x y : Event) : Set Event :=
  {z | Precedes x z ∧ Precedes y z}

noncomputable def futureMass (x y : Event) : ℝ≥0∞ :=
  uniform (commonFuture x y)

def motif : Set ((Event × Event) × (Event × Event)) :=
  {p | p.2 ∈ commonFuture p.1.1 p.1.2 ×ˢ commonFuture p.1.1 p.1.2}

theorem diamond_isOpen : IsOpen diamond := by
  unfold diamond
  exact (isOpen_lt (f := fun x : Event => ‖x.2‖)
    (g := fun x : Event => x.1) (by fun_prop) (by fun_prop)).inter
    (isOpen_lt (f := fun x : Event => ‖x.2‖)
      (g := fun x : Event => 1 - x.1) (by fun_prop) (by fun_prop))

theorem diamond_volume_pos : 0 < (volume : Measure Event) diamond := by
  apply diamond_isOpen.measure_pos volume
  refine ⟨(1 / 2, 0), ?_⟩
  change ‖(0 : EuclideanSpace ℝ (Fin 3))‖ < 1 / 2 ∧
    ‖(0 : EuclideanSpace ℝ (Fin 3))‖ < 1 - 1 / 2
  simp only [norm_zero]
  norm_num

theorem diamond_volume_lt_top : (volume : Measure Event) diamond < ∞ := by
  apply lt_of_le_of_lt (measure_mono (t := Metric.ball (0 : Event) 2) ?_)
    measure_ball_lt_top
  intro x hx
  change ‖x.2‖ < x.1 ∧ ‖x.2‖ < 1 - x.1 at hx
  have hpos : 0 ≤ x.1 := (norm_nonneg _).trans hx.1.le
  have ht : x.1 < 1 := by linarith [hx.2, norm_nonneg x.2]
  rw [Metric.mem_ball, dist_zero_right, Prod.norm_def, max_lt_iff, Real.norm_eq_abs,
    abs_of_nonneg hpos]
  exact ⟨ht.trans (by norm_num), hx.1.trans (ht.trans (by norm_num))⟩

instance : IsProbabilityMeasure uniform where
  measure_univ := by
    simpa [uniform] using ENNReal.inv_mul_cancel
      (ne_of_gt diamond_volume_pos) (ne_of_lt diamond_volume_lt_top)

theorem motif_measurable : MeasurableSet motif := by
  change MeasurableSet
    ({p : (Event × Event) × (Event × Event) | ‖p.2.1.2 - p.1.1.2‖ ≤ p.2.1.1 - p.1.1.1} ∩
      {p : (Event × Event) × (Event × Event) | ‖p.2.1.2 - p.1.2.2‖ ≤ p.2.1.1 - p.1.2.1} ∩
      ({p : (Event × Event) × (Event × Event) | ‖p.2.2.2 - p.1.1.2‖ ≤ p.2.2.1 - p.1.1.1} ∩
       {p : (Event × Event) × (Event × Event) | ‖p.2.2.2 - p.1.2.2‖ ≤ p.2.2.1 - p.1.2.1}))
  apply MeasurableSet.inter <;> apply MeasurableSet.inter <;>
    exact (isClosed_le (by fun_prop) (by fun_prop)).measurableSet

private theorem motif_fiber (p : Event × Event) :
    (Prod.mk p ⁻¹' motif) =
      commonFuture p.1 p.2 ×ˢ commonFuture p.1 p.2 := rfl

private theorem measurable_futureMass_sq :
    Measurable (fun p : Event × Event => futureMass p.1 p.2 ^ 2) := by
  have h := measurable_measure_prodMk_left
    (ν := uniform.prod uniform) motif_measurable
  simpa only [motif_fiber, Measure.prod_prod, pow_two, futureMass] using h

theorem motif_probability_eq_iterated_lintegral :
    ((uniform.prod uniform).prod (uniform.prod uniform)) motif =
      ∫⁻ x, ∫⁻ y, futureMass x y ^ 2 ∂uniform ∂uniform := by
  rw [Measure.prod_apply motif_measurable]
  simp_rw [motif_fiber, Measure.prod_prod, ← pow_two]
  exact lintegral_prod _ measurable_futureMass_sq.aemeasurable

theorem motif_probability_eq_iterated_integral :
    (((uniform.prod uniform).prod (uniform.prod uniform)) motif).toReal =
      ∫ x, ∫ y, (futureMass x y).toReal ^ 2 ∂uniform ∂uniform := by
  have hbound (x y : Event) : futureMass x y ^ 2 ≤ 1 := by
    have h : futureMass x y ≤ 1 := (measure_mono (subset_univ _)).trans_eq (measure_univ)
    simpa using pow_le_pow_left₀ (zero_le _) h 2
  have hi (x : Event) : (∫⁻ y, futureMass x y ^ 2 ∂uniform) ≤ 1 :=
    (lintegral_mono (fun y => hbound x y)).trans_eq (by simp)
  have hs (x : Event) :
      (∫ y, (futureMass x y).toReal ^ 2 ∂uniform) =
        (∫⁻ y, futureMass x y ^ 2 ∂uniform).toReal := by
    simpa only [pow_two, ENNReal.toReal_mul, Function.comp_apply, Prod.fst, Prod.snd] using
      (integral_toReal ((measurable_futureMass_sq.comp
        (measurable_prodMk_left (x := x))).aemeasurable)
        (Filter.Eventually.of_forall fun y => (hbound x y).trans_lt ENNReal.one_lt_top))
  rw [motif_probability_eq_iterated_lintegral]
  simp_rw [hs]
  exact (integral_toReal
    (measurable_futureMass_sq.lintegral_prod_right').aemeasurable
    (Filter.Eventually.of_forall fun x => (hi x).trans_lt ENNReal.one_lt_top)).symm

#print axioms motif_probability_eq_iterated_lintegral
#print axioms motif_probability_eq_iterated_integral

end Chronos.FourEvent
