import PhysicalMomentsBase
import Mathlib.MeasureTheory.Function.JacobianOneDim

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

open Chronos.NullCoordinates

noncomputable section

private theorem exp_lintegral
    (f : ℝ → ℝ≥0∞) :
    (∫⁻ u in Ioi (0 : ℝ), f u) =
      ∫⁻ a : ℝ,
        ENNReal.ofReal (Real.exp a) *
          f (Real.exp a) := by

  have himage :
      Real.exp '' (univ : Set ℝ) =
        Ioi (0 : ℝ) := by
    ext u
    constructor
    · rintro ⟨a,ha,rfl⟩
      exact Real.exp_pos a
    · intro hu
      exact ⟨Real.log u,mem_univ _,
        Real.exp_log hu⟩

  have hd :
      ∀ a ∈ (univ : Set ℝ),
        HasDerivWithinAt Real.exp
          (Real.exp a) univ a := by
    intro a ha
    exact (Real.hasDerivAt_exp a).hasDerivWithinAt

  have hm :
      MonotoneOn Real.exp (univ : Set ℝ) :=
    Real.exp_monotone.monotoneOn (univ : Set ℝ)

  have h :=
    lintegral_image_eq_lintegral_deriv_mul_of_monotoneOn
      (show MeasurableSet (univ : Set ℝ)
        from isOpen_univ.measurableSet) hd hm f

  rw [himage,Measure.restrict_univ] at h

  exact h

private def expPair (p : Plane) : Plane :=
  (Real.exp p.1,Real.exp p.2)

private theorem expPair_measurable :
    Measurable expPair := by
  unfold expPair
  fun_prop

private theorem exp_pair_integral
    (F : Plane → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p in
      Ioi (0 : ℝ) ×ˢ Ioi (0 : ℝ), F p) =
      ∫⁻ p : Plane,
        ENNReal.ofReal
          (Real.exp (p.1+p.2)) *
          F (expPair p) := by

  let nu : Measure ℝ :=
    volume.restrict (Ioi (0 : ℝ))

  have hp :
      (volume : Measure Plane).restrict
        (Ioi (0 : ℝ) ×ˢ Ioi (0 : ℝ)) =
          nu.prod nu := by
    unfold nu
    rw [Measure.volume_eq_prod,
      Measure.prod_restrict]

  have hk :
      Measurable
        (fun p : Plane =>
          ENNReal.ofReal
            (Real.exp (p.1+p.2)) *
            F (expPair p)) := by
    unfold expPair
    fun_prop

  calc
    _ = ∫⁻ u : ℝ, ∫⁻ v : ℝ,
        F (u,v) ∂nu ∂nu := by
      rw [hp]
      exact lintegral_prod _ hF.aemeasurable

    _ = ∫⁻ a : ℝ,
        ENNReal.ofReal (Real.exp a) *
          (∫⁻ v : ℝ,
            F (Real.exp a,v) ∂nu) := by
      exact exp_lintegral
        (fun u => ∫⁻ v : ℝ, F (u,v) ∂nu)

    _ = ∫⁻ a : ℝ,
        ENNReal.ofReal (Real.exp a) *
          (∫⁻ b : ℝ,
            ENNReal.ofReal (Real.exp b) *
              F (Real.exp a,Real.exp b)) := by
      apply lintegral_congr
      intro a
      rw [show
        (∫⁻ v : ℝ, F (Real.exp a,v) ∂nu) =
        (∫⁻ b : ℝ,
          ENNReal.ofReal (Real.exp b) *
            F (Real.exp a,Real.exp b))
        from exp_lintegral
          (fun v => F (Real.exp a,v))]

    _ = ∫⁻ a : ℝ, ∫⁻ b : ℝ,
        ENNReal.ofReal (Real.exp (a+b)) *
          F (Real.exp a,Real.exp b) := by
      apply lintegral_congr
      intro a

      have hm :
          Measurable
            (fun b : ℝ =>
              ENNReal.ofReal (Real.exp b) *
                F (Real.exp a,Real.exp b)) := by
        fun_prop

      rw [← lintegral_const_mul _ hm]

      apply lintegral_congr
      intro b

      rw [Real.exp_add,
        ENNReal.ofReal_mul
          (Real.exp_pos a).le,mul_assoc]

    _ = _ := by
      rw [Measure.volume_eq_prod,
        lintegral_prod _ hk.aemeasurable]

      rfl

def rapidityNull (p : Plane) : Plane :=
  expPair (nullLinear p)

def rapidityRegion : Set Plane :=
  {p | 0 < p.2 ∧ p.2 < p.1}

private theorem rapidityRegion_measurable :
    MeasurableSet rapidityRegion := by
  exact
    (isOpen_lt
      (f := fun _ : Plane => (0 : ℝ))
      (g := fun p : Plane => p.2)
      continuous_const
      continuous_snd).measurableSet.inter
    (isOpen_lt
      (f := fun p : Plane => p.2)
      (g := fun p : Plane => p.1)
      continuous_snd
      continuous_fst).measurableSet

theorem rapidityNull_domain
    (p : Plane) :
    rapidityNull p ∈ triangle ↔
      p ∈ rapidityRegion := by

  change
    (0 < Real.exp (-p.1-p.2) ∧
      Real.exp (-p.1-p.2) <
        Real.exp (-p.1+p.2) ∧
      Real.exp (-p.1+p.2) < 1) ↔
      (0 < p.2 ∧ p.2 < p.1)

  have ht :
      Real.exp (-p.1+p.2) < 1 ↔
        -p.1+p.2 < 0 := by
    simpa only [Real.exp_zero] using
      (show
        Real.exp (-p.1+p.2) < Real.exp 0 ↔
          -p.1+p.2 < 0
        from Real.exp_lt_exp)

  rw [Real.exp_lt_exp,ht]

  constructor
  · rintro ⟨h0,h1,h2⟩
    exact ⟨by linarith,by linarith⟩
  · rintro ⟨h1,h2⟩
    exact ⟨Real.exp_pos _,
      by linarith,by linarith⟩

theorem null_rapidity_integral
    (F : Plane → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p in triangle,F p) =
      ∫⁻ q in rapidityRegion,
        ENNReal.ofReal
          (2*Real.exp (-2*q.1)) *
          F (rapidityNull q) := by

  let G : Plane → ℝ≥0∞ :=
    triangle.indicator F

  have hG : Measurable G :=
    hF.indicator triangle_measurable

  let H : Plane → ℝ≥0∞ :=
    fun p =>
      ENNReal.ofReal
        (Real.exp (p.1+p.2)) *
        G (expPair p)

  have hH : Measurable H := by
    unfold H expPair
    fun_prop

  have hsub :
      triangle ⊆
        Ioi (0 : ℝ) ×ˢ Ioi (0 : ℝ) := by
    intro p hp

    change
      0 < p.1 ∧ p.1 < p.2 ∧ p.2 < 1
      at hp

    exact ⟨hp.1,hp.1.trans hp.2.1⟩

  have hexp :
      (∫⁻ p in triangle,F p) =
        ∫⁻ p : Plane,H p := by
    calc
      _ = ∫⁻ p in
          Ioi (0 : ℝ) ×ˢ Ioi (0 : ℝ),
          G p := by

        unfold G

        rw [lintegral_indicator
          triangle_measurable,
          Measure.restrict_restrict_of_subset
            hsub]

      _ = _ := exp_pair_integral G hG

  letI : (volume : Measure Plane).IsAddHaarMeasure := by
    rw [Measure.volume_eq_prod]
    infer_instance

  have hdet :
      LinearMap.det nullLinear ≠ 0 := by
    intro hz
    have hh := nullLinear_abs_det
    rw [hz,abs_zero] at hh
    norm_num at hh

  have hmap :
      (volume : Measure Plane).map nullLinear =
        ENNReal.ofReal (1/2 : ℝ) •
          (volume : Measure Plane) := by

    have hh :=
      Measure.map_linearMap_addHaar_eq_smul_addHaar
        (volume : Measure Plane) hdet

    rw [abs_inv,nullLinear_abs_det] at hh

    simpa only [one_div] using hh

  have hL :
      Measurable (nullLinear : Plane → Plane) := by
    change Measurable
      (fun p : Plane =>
        (-p.1-p.2,-p.1+p.2))
    fun_prop

  have hmeasure :=
    lintegral_map
      (μ := (volume : Measure Plane))
      hH hL

  rw [hmap,lintegral_smul_measure,
    smul_eq_mul] at hmeasure

  have htwo :
      ENNReal.ofReal (2 : ℝ) *
        ENNReal.ofReal (1/2 : ℝ) = 1 := by
    rw [← ENNReal.ofReal_mul
      (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num

  have hscale :
      (∫⁻ p : Plane,H p) =
        ∫⁻ q : Plane,
          ENNReal.ofReal (2 : ℝ) *
            H (nullLinear q) := by
    have hm :
        Measurable (fun q : Plane =>
          H (nullLinear q)) :=
      hH.comp hL

    calc
      _ = 1 * (∫⁻ p : Plane,H p) :=
        (one_mul _).symm
      _ = ENNReal.ofReal (2 : ℝ) *
          (ENNReal.ofReal (1/2 : ℝ) *
            (∫⁻ p : Plane,H p)) := by
        rw [← mul_assoc,htwo]
      _ = ENNReal.ofReal (2 : ℝ) *
          (∫⁻ q : Plane,H (nullLinear q)) := by
        rw [hmeasure]
      _ = _ :=
        (lintegral_const_mul
          (ENNReal.ofReal (2 : ℝ)) hm).symm

  rw [hexp,hscale,
    ← lintegral_indicator
      rapidityRegion_measurable]

  apply lintegral_congr
  intro q

  have hsum :
      (nullLinear q).1+(nullLinear q).2 =
        -2*q.1 := by
    change
      (-q.1-q.2)+(-q.1+q.2) =
        -2*q.1
    ring

  unfold H

  rw [hsum,← mul_assoc,
    ← ENNReal.ofReal_mul
      (by norm_num : (0 : ℝ) ≤ 2)]

  change
    ENNReal.ofReal
      (2*Real.exp (-2*q.1)) *
        G (rapidityNull q) =
      rapidityRegion.indicator
        (fun z =>
          ENNReal.ofReal
            (2*Real.exp (-2*z.1)) *
            F (rapidityNull z)) q

  by_cases hq : q ∈ rapidityRegion

  · have ht :
        rapidityNull q ∈ triangle :=
      (rapidityNull_domain q).mpr hq

    rw [Set.indicator_of_mem hq]

    unfold G

    rw [Set.indicator_of_mem ht]

  · have ht :
        rapidityNull q ∉ triangle := by
      intro h
      exact hq ((rapidityNull_domain q).mp h)

    rw [Set.indicator_of_notMem hq]

    unfold G

    rw [Set.indicator_of_notMem ht,mul_zero]

#print axioms rapidityNull_domain
#print axioms null_rapidity_integral

end

end Chronos.FourEvent
