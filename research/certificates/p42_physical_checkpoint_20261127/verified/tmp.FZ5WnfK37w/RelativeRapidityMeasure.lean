import PhysicalRapidityMeasure
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.MeasureTheory.Function.JacobianOneDim

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

noncomputable section

def relativeCos (x z e : ℝ) : ℝ :=
  (Real.cosh e -
    Real.cosh x * Real.cosh z) /
      (Real.sinh x * Real.sinh z)

private theorem denominator_pos
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z) :
    0 < Real.sinh x * Real.sinh z :=
  mul_pos
    (Real.sinh_pos_iff.mpr hx)
    (Real.sinh_pos_iff.mpr hz)

theorem relativeCos_endpoints
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z) :
    relativeCos x z |x-z| = -1 ∧
    relativeCos x z (x+z) = 1 := by

  have hd :=
    denominator_pos x z hx hz

  constructor

  · unfold relativeCos
    rw [Real.cosh_abs,Real.cosh_sub]
    field_simp [hd.ne'] <;> ring

  · unfold relativeCos
    rw [Real.cosh_add]
    field_simp [hd.ne'] <;> ring

private theorem relativeCos_strict
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z) :
    StrictMonoOn
      (relativeCos x z)
      (Icc |x-z| (x+z)) := by

  intro a ha b hb hab

  have ha0 : 0 ≤ a :=
    (abs_nonneg (x-z)).trans ha.1

  have hb0 : 0 ≤ b :=
    (abs_nonneg (x-z)).trans hb.1

  have hc : Real.cosh a < Real.cosh b := by

    apply Real.cosh_lt_cosh.mpr

    rwa [abs_of_nonneg ha0,
      abs_of_nonneg hb0]

  unfold relativeCos

  exact div_lt_div_of_pos_right
    (sub_lt_sub_right hc _)
    (denominator_pos x z hx hz)

theorem relativeCos_image
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z) :
    relativeCos x z ''
      Ioo |x-z| (x+z) =
        Ioo (-1 : ℝ) 1 := by

  let a : ℝ := |x-z|
  let b : ℝ := x+z
  let f : ℝ → ℝ := relativeCos x z

  have hab : a < b := by
    dsimp only [a,b]
    apply abs_lt.mpr
    constructor <;> linarith

  have hfa : f a = -1 :=
    (relativeCos_endpoints x z hx hz).1

  have hfb : f b = 1 :=
    (relativeCos_endpoints x z hx hz).2

  have hs : StrictMonoOn f (Icc a b) :=
    relativeCos_strict x z hx hz

  have hcont : Continuous f := by
    unfold f relativeCos
    fun_prop

  change f '' Ioo a b = Ioo (-1 : ℝ) 1

  ext c
  constructor

  · rintro ⟨e,he,rfl⟩

    have hea : a ∈ Icc a b :=
      ⟨le_rfl,hab.le⟩

    have heb : b ∈ Icc a b :=
      ⟨hab.le,le_rfl⟩

    have hec : e ∈ Icc a b :=
      ⟨he.1.le,he.2.le⟩

    have hlow : f a < f e :=
      hs hea hec he.1

    have hhigh : f e < f b :=
      hs hec heb he.2

    rw [hfa] at hlow
    rw [hfb] at hhigh

    exact ⟨hlow,hhigh⟩

  · intro hc

    have hcc : c ∈ Icc (f a) (f b) := by
      rw [hfa,hfb]
      exact ⟨hc.1.le,hc.2.le⟩

    have himage :=
      intermediate_value_Icc
        hab.le hcont.continuousOn hcc

    obtain ⟨e,he,hef⟩ := himage

    have hne1 : a ≠ e := by
      intro h
      have hbad : f a = c :=
        h ▸ hef
      rw [hfa] at hbad
      exact hc.1.ne hbad

    have hne2 : e ≠ b := by
      intro h
      have hbad : f b = c :=
        h ▸ hef
      rw [hfb] at hbad
      exact hc.2.ne hbad.symm

    exact ⟨e,
      ⟨lt_of_le_of_ne he.1 hne1,
        lt_of_le_of_ne he.2 hne2⟩,
      hef⟩

theorem relative_rapidity_lintegral
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z)
    (F : ℝ → ℝ≥0∞) :
    (∫⁻ c in Ioo (-1 : ℝ) 1,F c) =
      ∫⁻ e in Ioo |x-z| (x+z),
        ENNReal.ofReal
          (Real.sinh e /
            (Real.sinh x * Real.sinh z)) *
          F (relativeCos x z e) := by

  let S : Set ℝ :=
    Ioo |x-z| (x+z)

  have hd :
      ∀ e ∈ S,
        HasDerivWithinAt
          (relativeCos x z)
          (Real.sinh e /
            (Real.sinh x * Real.sinh z))
          S e := by

    intro e he

    unfold relativeCos

    exact
      (((Real.hasDerivAt_cosh e).sub_const
        (Real.cosh x * Real.cosh z)).div_const
        (Real.sinh x * Real.sinh z)).hasDerivWithinAt

  have hs :
      StrictMonoOn
        (relativeCos x z)
        (Icc |x-z| (x+z)) :=
    relativeCos_strict x z hx hz

  have hm :
      MonotoneOn (relativeCos x z) S := by

    intro a ha b hb hab

    have hac : a ∈ Icc |x-z| (x+z) :=
      ⟨ha.1.le,ha.2.le⟩

    have hbc : b ∈ Icc |x-z| (x+z) :=
      ⟨hb.1.le,hb.2.le⟩

    rcases lt_or_eq_of_le hab with h | h

    · exact (hs hac hbc h).le
    · subst b
      exact le_rfl

  have hS : MeasurableSet S :=
    measurableSet_Ioo

  have h :=
    lintegral_image_eq_lintegral_deriv_mul_of_monotoneOn
      hS hd hm F

  have himage :
      relativeCos x z '' S =
        Ioo (-1 : ℝ) 1 :=
    relativeCos_image x z hx hz

  rw [himage] at h

  exact h

#print axioms relativeCos_endpoints
#print axioms relativeCos_image
#print axioms relative_rapidity_lintegral

end

end Chronos.FourEvent
