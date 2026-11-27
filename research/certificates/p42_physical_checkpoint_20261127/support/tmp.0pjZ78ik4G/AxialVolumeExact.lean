import AxialDiskSlicing
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

open Set MeasureTheory
open scoped ENNReal

namespace Chronos.FourEvent

noncomputable section

private def G (T A B : ℝ) : ℝ :=
  T^3/12 - T*(A^2+B^2)/2 -
    (A^2-B^2)^2/(4*T) +
    2*(A^3+B^3)/3

private def poly (c0 c1 c2 c3 x : ℝ) : ℝ :=
  c0 + c1*x + c2*x^2 + c3*x^3

private def prim (c0 c1 c2 c3 x : ℝ) : ℝ :=
  c0*x + c1*x^2/2 + c2*x^3/3 + c3*x^4/4

private theorem poly_integral
    (c0 c1 c2 c3 l r : ℝ) :
    (∫ x in l..r, poly c0 c1 c2 c3 x) =
      prim c0 c1 c2 c3 r -
      prim c0 c1 c2 c3 l := by
  have h0 : IntervalIntegrable
      (fun _ : ℝ => c0) volume l r :=
    continuous_const.intervalIntegrable _ _
  have h1 : IntervalIntegrable
      (fun x : ℝ => c1*x) volume l r :=
    (show Continuous (fun x : ℝ => c1*x) by
      fun_prop).intervalIntegrable _ _
  have h2 : IntervalIntegrable
      (fun x : ℝ => c2*x^2) volume l r :=
    (show Continuous (fun x : ℝ => c2*x^2) by
      fun_prop).intervalIntegrable _ _
  have h3 : IntervalIntegrable
      (fun x : ℝ => c3*x^3) volume l r :=
    (show Continuous (fun x : ℝ => c3*x^3) by
      fun_prop).intervalIntegrable _ _
  unfold poly prim
  rw [intervalIntegral.integral_add
        ((h0.add h1).add h2) h3,
      intervalIntegral.integral_add (h0.add h1) h2,
      intervalIntegral.integral_add h0 h1]
  simp [intervalIntegral.integral_const_mul,
    integral_id, integral_pow, smul_eq_mul] <;> ring

private theorem lintegral_cut
    (f : ℝ → ℝ) (g : ℝ → ℝ≥0∞)
    (l r : ℝ) (hlr : l ≤ r)
    (hc : Continuous f)
    (hn : ∀ x ∈ Icc l r, 0 ≤ f x)
    (hg : ∀ x, g x =
      if l ≤ x ∧ x ≤ r then ENNReal.ofReal (f x)
      else 0) :
    (∫⁻ x, g x) =
      ENNReal.ofReal (∫ x in l..r, f x) := by
  have hi :
      IntegrableOn f (Icc l r) volume :=
    (intervalIntegrable_iff_integrableOn_Icc_of_le
      hlr).mp (hc.intervalIntegrable _ _)
  have hnn :
      0 ≤ᵐ[volume.restrict (Icc l r)] f :=
    (ae_restrict_iff' measurableSet_Icc).mpr
      (Filter.Eventually.of_forall hn)
  calc
    _ = ∫⁻ x, (Icc l r).indicator
        (fun y => ENNReal.ofReal (f y)) x := by
      apply lintegral_congr
      intro x
      rw [hg]
      simp [Set.indicator, mem_Icc]
    _ = ∫⁻ x in Icc l r, ENNReal.ofReal (f x) :=
      lintegral_indicator measurableSet_Icc _
    _ = _ := by
      rw [intervalIntegral.integral_of_le hlr,
        ← integral_Icc_eq_integral_Ioc]
      exact
        (ofReal_integral_eq_lintegral_ofReal
          hi hnn).symm

private def timeArea (T A B s : ℝ) : ℝ≥0∞ :=
  if 0 ≤ s ∧ s ≤ T then
    ENNReal.ofReal
      (min (s^2-A^2) ((T-s)^2-B^2)*Real.pi)
  else 0

private theorem timeArea_support
    (T A B s : ℝ) (hA : 0 ≤ A) (hB : 0 ≤ B) :
    timeArea T A B s =
      if A ≤ s ∧ s ≤ T-B then
        ENNReal.ofReal
          (min (s^2-A^2) ((T-s)^2-B^2)*Real.pi)
      else 0 := by
  by_cases hs : A ≤ s ∧ s ≤ T-B
  · have ht : 0 ≤ s ∧ s ≤ T :=
      ⟨hA.trans hs.1, by linarith [hs.2]⟩
    simp [timeArea, hs, ht]
  · rw [if_neg hs]
    unfold timeArea
    split_ifs with ht
    · apply ENNReal.ofReal_eq_zero.mpr
      apply mul_nonpos_of_nonpos_of_nonneg _
        Real.pi_nonneg
      by_cases h : A ≤ s
      · have hb : T-B < s := by
          by_contra! hh
          exact hs ⟨h,hh⟩
        apply (min_le_right _ _).trans
        apply sub_nonpos.mpr
        exact (sq_le_sq₀
          (sub_nonneg.mpr ht.2) hB).mpr
            (by linarith)
      · apply (min_le_left _ _).trans
        apply sub_nonpos.mpr
        exact (sq_le_sq₀ ht.1 hA).mpr
          (le_of_not_ge h)

private theorem time_integral
    (T A B : ℝ) (hT : 0 < T)
    (hA : 0 ≤ A) (hB : 0 ≤ B) :
    (∫⁻ s, timeArea T A B s) =
      if A+B ≤ T then
        ENNReal.ofReal (G T A B * Real.pi)
      else 0 := by
  by_cases hab : A+B ≤ T
  · rw [if_pos hab]
    let f : ℝ → ℝ := fun s =>
      min (s^2-A^2) ((T-s)^2-B^2)*Real.pi
    have hcont : Continuous f := by
      dsimp [f]
      fun_prop
    have hnon : ∀ s ∈ Icc A (T-B), 0 ≤ f s := by
      intro s hs
      dsimp [f]
      apply mul_nonneg _ Real.pi_nonneg
      apply le_min
      · exact sub_nonneg.mpr
          ((sq_le_sq₀ hA
            (hA.trans hs.1)).mpr hs.1)
      · exact sub_nonneg.mpr
          ((sq_le_sq₀ hB (by linarith [hs.2])).mpr
            (by linarith [hs.2]))
    rw [lintegral_cut f (timeArea T A B) A (T-B)
      (by linarith) hcont hnon
      (fun s => timeArea_support T A B s hA hB)]
    let c := (T^2+A^2-B^2)/(2*T)
    have hgap : 0 ≤ T-A-B := by linarith
    have hc1 : A ≤ c := by
      dsimp [c]
      apply (le_div_iff₀ (by positivity)).mpr
      nlinarith [mul_nonneg hgap
        (show 0 ≤ T-A+B by linarith)]
    have hc2 : c ≤ T-B := by
      dsimp [c]
      apply (div_le_iff₀ (by positivity)).mpr
      nlinarith [mul_nonneg hgap
        (show 0 ≤ T-B+A by linarith)]
    let k : ℝ → ℝ := fun s =>
      min (s^2-A^2) ((T-s)^2-B^2)
    have hk : Continuous k := by
      dsimp [k]
      fun_prop
    have hleft :
        (∫ s in A..c, k s) =
          prim (-A^2) 0 1 0 c -
          prim (-A^2) 0 1 0 A := by
      rw [← poly_integral (-A^2) 0 1 0 A c]
      apply intervalIntegral.integral_congr
      intro s hs
      rw [uIcc_of_le hc1] at hs
      have hle : s^2-A^2 ≤ (T-s)^2-B^2 := by
        have hh := hs.2
        change s ≤ (T^2+A^2-B^2)/(2*T) at hh
        have hh' :=
          (le_div_iff₀ (show 0 < 2*T by positivity)).mp hh
        nlinarith
      dsimp [k,poly]
      rw [min_eq_left hle]
      ring
    have hright :
        (∫ s in c..(T-B), k s) =
          prim (T^2-B^2) (-2*T) 1 0 (T-B) -
          prim (T^2-B^2) (-2*T) 1 0 c := by
      rw [← poly_integral (T^2-B^2) (-2*T) 1 0 c (T-B)]
      apply intervalIntegral.integral_congr
      intro s hs
      rw [uIcc_of_le hc2] at hs
      have hle : (T-s)^2-B^2 ≤ s^2-A^2 := by
        have hh := hs.1
        change (T^2+A^2-B^2)/(2*T) ≤ s at hh
        have hh' :=
          (div_le_iff₀ (show 0 < 2*T by positivity)).mp hh
        nlinarith
      dsimp [k,poly]
      rw [min_eq_right hle]
      ring
    have hsplit :=
      intervalIntegral.integral_add_adjacent_intervals
        (hk.intervalIntegrable A c)
        (hk.intervalIntegrable c (T-B))
    change ENNReal.ofReal
        (∫ s in A..(T-B), k s * Real.pi) = _
    rw [intervalIntegral.integral_mul_const,
      ← hsplit,hleft,hright]
    congr 1
    dsimp [prim,c,G]
    field_simp [ne_of_gt hT] <;> ring
  · rw [if_neg hab]
    have hz : ∀ s, timeArea T A B s = 0 := by
      intro s
      rw [timeArea_support T A B s hA hB]
      apply if_neg
      intro hs
      exact hab (by linarith [hs.1,hs.2])
    simp [hz]

private theorem section_eq_time
    (a b T s x : ℝ) (ha : 0 ≤ a) :
    sectionArea a b T s x =
      timeArea T (a+|x|) |x-b| s := by
  have hm :
      min (s^2-(x+a)^2) (s^2-(x-a)^2) =
        s^2-(a+|x|)^2 := by
    rcases le_total 0 x with hx | hx
    · rw [abs_of_nonneg hx,
        min_eq_left (show
          s^2-(x+a)^2 ≤ s^2-(x-a)^2 by
            nlinarith [mul_nonneg ha hx])]
      ring
    · rw [abs_of_nonpos hx,
        min_eq_right (show
          s^2-(x-a)^2 ≤ s^2-(x+a)^2 by
            nlinarith [mul_nonneg ha
              (neg_nonneg.mpr hx)])]
      ring
  unfold sectionArea sectionRadiusSq timeArea
  rw [← min_assoc,hm,sq_abs]

private theorem volume_disk_integral (a b T : ℝ) :
    (volume : Measure Event) (axialLens a b T) =
      ∫⁻ x : ℝ, ∫⁻ s : ℝ, sectionArea a b T s x := by
  have hm : MeasurableSet (axialLens a b T) := by
    change MeasurableSet
      ({z : Event | ‖z.2-axis (-a)‖ ≤ z.1-0} ∩
        ({z : Event | ‖z.2-axis a‖ ≤ z.1-0} ∩
          {z : Event | ‖axis b-z.2‖ ≤ T-z.1}))
    exact
      (isClosed_le (by fun_prop) (by fun_prop)).measurableSet.inter
        ((isClosed_le (by fun_prop) (by fun_prop)).measurableSet.inter
          (isClosed_le (by fun_prop) (by fun_prop)).measurableSet)
  rw [Measure.volume_eq_prod, Measure.prod_apply hm]
  calc
    _ = ∫⁻ s : ℝ, ∫⁻ x : ℝ, sectionArea a b T s x := by
      apply lintegral_congr
      intro s
      let E : Set Space :=
        Prod.mk s ⁻¹' axialLens a b T
      have hE : MeasurableSet E :=
        measurable_prodMk_left hm
      have hp :=
        pack_measurePreserving.measure_preimage
          hE.nullMeasurableSet
      change (volume : Measure Space) E = _
      rw [← hp, Measure.volume_eq_prod,
        Measure.prod_apply
          (pack_measurePreserving.measurable hE)]
      apply lintegral_congr
      intro x
      exact axial_transverse_slice a b T s x
    _ = _ := by
      let f : ℝ × ℝ → ℝ≥0∞ := fun p =>
        sectionArea a b T p.1 p.2
      have hf : Measurable f := by
        dsimp [f,sectionArea,sectionRadiusSq]
        apply Measurable.ite
        · exact
            (isClosed_le (by fun_prop)
              (by fun_prop)).measurableSet.inter
            (isClosed_le (by fun_prop)
              (by fun_prop)).measurableSet
        · fun_prop
        · exact measurable_const
      exact (lintegral_prod f hf.aemeasurable).symm.trans
        (lintegral_prod_symm f hf.aemeasurable)

private def C0 (T A B : ℝ) : ℝ := G T A B

private def C1 (T A B p q : ℝ) : ℝ :=
  -T*(A*p+B*q) -
    (A^2-B^2)*(A*p-B*q)/T +
    2*(A^2*p+B^2*q)

private def C2 (T A B p q : ℝ) : ℝ :=
  -T-(A*p-B*q)^2/T+2*(A+B)

private def C3 (p q : ℝ) : ℝ :=
  2*(p+q)/3

private def P (T A B p q x : ℝ) : ℝ :=
  prim (C0 T A B) (C1 T A B p q)
    (C2 T A B p q) (C3 p q) x

private theorem affine_integral
    (T A B p q l r : ℝ) (hT : 0 < T)
    (hp : p = 1 ∨ p = -1)
    (hq : q = 1 ∨ q = -1) :
    (∫ x in l..r, G T (A+p*x) (B+q*x)) =
      P T A B p q r-P T A B p q l := by
  unfold P
  rw [← poly_integral]
  apply intervalIntegral.integral_congr
  intro x _
  rcases hp with rfl | rfl <;>
    rcases hq with rfl | rfl <;>
    unfold poly C0 C1 C2 C3 G <;>
    field_simp [ne_of_gt hT] <;> ring

theorem axialLens_volume_exact
    (a b T : ℝ) (ha : 0 < a) (hb : 0 ≤ b)
    (hT : a+b < T) :
    (volume : Measure Event) (axialLens a b T) =
      ENNReal.ofReal
        (Real.pi*(T+2*a)*((T-a)^2-b^2)^2/(24*T)) := by
  have ht : 0 < T := by linarith
  let l := -(T-a-b)/2
  let r := (T-a+b)/2
  have hl : l ≤ 0 := by dsimp [l]; linarith
  have hr : b ≤ r := by dsimp [r]; linarith
  have hlr : l ≤ r := by linarith
  let f : ℝ → ℝ := fun x =>
    G T (a+|x|) |x-b|
  have hf : Continuous f := by
    dsimp [f,G]
    fun_prop
  have hsupp (x : ℝ) :
      a+|x|+|x-b| ≤ T ↔ l ≤ x ∧ x ≤ r := by
    dsimp [l,r]
    rcases le_total x 0 with hx | hx
    · rw [abs_of_nonpos hx,
        abs_of_nonpos (show x-b ≤ 0 by linarith)]
      constructor
      · intro h
        constructor <;> linarith
      · intro h
        linarith [h.1]
    · rcases le_total x b with hxb | hxb
      · rw [abs_of_nonneg hx,
          abs_of_nonpos (show x-b ≤ 0 by linarith)]
        constructor
        · intro h
          constructor <;> linarith
        · intro _
          linarith
      · rw [abs_of_nonneg hx,
          abs_of_nonneg (show 0 ≤ x-b by linarith)]
        constructor
        · intro h
          constructor <;> linarith
        · intro h
          linarith [h.2]
  have hn : ∀ x ∈ Icc l r, 0 ≤ f x := by
    intro x hx
    let A := a+|x|
    let B := |x-b|
    have hA : 0 ≤ A := by dsimp [A]; positivity
    have hB : 0 ≤ B := abs_nonneg _
    have hh : 0 ≤ T-A-B := by
      have hs := (hsupp x).mpr hx
      dsimp [A,B]
      linarith
    have hfact :
        G T A B =
          (T-A-B)^2*
            (12*A*B+4*(A+B)*(T-A-B)+(T-A-B)^2)/
            (12*T) := by
      unfold G
      field_simp [ne_of_gt ht] <;> ring
    change 0 ≤ G T A B
    rw [hfact]
    positivity
  rw [volume_disk_integral]
  have hi (x : ℝ) :
      (∫⁻ s, sectionArea a b T s x) =
        if l ≤ x ∧ x ≤ r then
          ENNReal.ofReal (f x*Real.pi)
        else 0 := by
    simp_rw [section_eq_time a b T _ x ha.le]
    rw [time_integral T (a+|x|) |x-b| ht
      (by positivity) (abs_nonneg _), hsupp]
    rfl
  rw [lintegral_cut
    (fun x => f x*Real.pi)
    (fun x => ∫⁻ s, sectionArea a b T s x)
    l r hlr (by fun_prop)
    (fun x hx => mul_nonneg (hn x hx) Real.pi_nonneg)
    hi]
  rw [intervalIntegral.integral_mul_const]
  have hparts :
      ((∫ x in l..0, f x) + (∫ x in 0..b, f x)) +
        (∫ x in b..r, f x) =
          ∫ x in l..r, f x := by
    rw [intervalIntegral.integral_add_adjacent_intervals
      (hf.intervalIntegrable l 0)
      (hf.intervalIntegrable 0 b),
      intervalIntegral.integral_add_adjacent_intervals
      (hf.intervalIntegrable l b)
      (hf.intervalIntegrable b r)]
  have hleft :
      (∫ x in l..0, f x) =
        ∫ x in l..0, G T (a+(-1)*x) (b+(-1)*x) := by
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le hl] at hx
    dsimp [f]
    rw [abs_of_nonpos hx.2,
      abs_of_nonpos (show x-b ≤ 0 by linarith [hx.2])]
    congr 1 <;> ring
  have hmid :
      (∫ x in 0..b, f x) =
        ∫ x in 0..b, G T (a+1*x) (b+(-1)*x) := by
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le hb] at hx
    dsimp [f]
    rw [abs_of_nonneg hx.1,
      abs_of_nonpos (show x-b ≤ 0 by linarith [hx.2])]
    congr 1 <;> ring
  have hright :
      (∫ x in b..r, f x) =
        ∫ x in b..r, G T (a+1*x) (-b+1*x) := by
    apply intervalIntegral.integral_congr
    intro x hx
    rw [uIcc_of_le hr] at hx
    dsimp [f]
    rw [abs_of_nonneg (hb.trans hx.1),
      abs_of_nonneg (show 0 ≤ x-b by linarith [hx.1])]
    congr 1 <;> ring
  rw [← hparts,hleft,hmid,hright,
    affine_integral T a b (-1) (-1) l 0 ht
      (Or.inr rfl) (Or.inr rfl),
    affine_integral T a b 1 (-1) 0 b ht
      (Or.inl rfl) (Or.inr rfl),
    affine_integral T a (-b) 1 1 b r ht
      (Or.inl rfl) (Or.inl rfl)]
  congr 1
  dsimp [P,prim,C0,C1,C2,C3,G,l,r]
  field_simp [ne_of_gt ht] <;> ring

#print axioms axialLens_volume_exact

end

end Chronos.FourEvent
