import MinkowskiMotif
import InvariantVolume

open Set MeasureTheory
open scoped ENNReal

namespace Chronos.FourEvent

abbrev Space := EuclideanSpace ℝ (Fin 3)

noncomputable def axis (a : ℝ) : Space := PiLp.single 2 0 a

def axialLens (a b T : ℝ) : Set Event :=
  {z | Precedes (0, axis (-a)) z ∧ Precedes (0, axis a) z ∧
    Precedes z (T, axis b)}

noncomputable def axialWidth (a b T : ℝ) (w : Space) : ℝ :=
  T - ‖axis b - w‖ - max ‖w - axis (-a)‖ ‖w - axis a‖

theorem axialLens_volume_eq_lintegral (a b T : ℝ) :
    (volume : Measure Event) (axialLens a b T) =
      ∫⁻ w : Space, ENNReal.ofReal (axialWidth a b T w) := by
  have hm : MeasurableSet (axialLens a b T) := by
    change MeasurableSet
      ({z : Event | ‖z.2 - axis (-a)‖ ≤ z.1 - 0} ∩
       ({z : Event | ‖z.2 - axis a‖ ≤ z.1 - 0} ∩
        {z : Event | ‖axis b - z.2‖ ≤ T - z.1}))
    apply MeasurableSet.inter
    · exact (isClosed_le (by fun_prop) (by fun_prop)).measurableSet
    · apply MeasurableSet.inter <;>
        exact (isClosed_le (by fun_prop) (by fun_prop)).measurableSet
  rw [Measure.volume_eq_prod, Measure.prod_apply_symm hm]
  apply lintegral_congr
  intro w
  have hfiber :
      ((fun s : ℝ => (s, w)) ⁻¹' axialLens a b T) =
        Icc (max ‖w - axis (-a)‖ ‖w - axis a‖) (T - ‖axis b - w‖) := by
    ext s
    change (‖w - axis (-a)‖ ≤ s - 0 ∧ ‖w - axis a‖ ≤ s - 0 ∧
      ‖axis b - w‖ ≤ T - s) ↔
        max ‖w - axis (-a)‖ ‖w - axis a‖ ≤ s ∧ s ≤ T - ‖axis b - w‖
    simp only [sub_zero, max_le_iff]
    constructor
    · rintro ⟨hl, hr, hu⟩
      exact ⟨⟨hl, hr⟩, by linarith⟩
    · rintro ⟨⟨hl, hr⟩, hu⟩
      exact ⟨hl, hr, by linarith⟩
  rw [hfiber, Real.volume_Icc]
  rfl

#print axioms axialLens_volume_eq_lintegral

end Chronos.FourEvent
