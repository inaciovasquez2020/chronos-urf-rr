import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic.Module
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic.Ring
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.Tactic



open MeasureTheory Set
open scoped ENNReal

namespace Chronos.GeometricTransport

variable {α β : Type*}
variable [MeasurableSpace α] [MeasurableSpace β]

noncomputable def normalized (μ : Measure α) :
    Measure α :=
  (μ Set.univ)⁻¹ • μ

theorem normalized_map
    (μ : Measure α) (ν : Measure β)
    (f : α → β) (c : ℝ≥0∞)
    (hf : Measurable f)
    (hc0 : c ≠ 0)
    (hcT : c ≠ ∞)
    (hmap : μ.map f = c • ν) :
    (normalized μ).map f = normalized ν := by
  have hmass :
      μ Set.univ = c * ν Set.univ := by
    calc
      μ Set.univ = (μ.map f) Set.univ := by
        rw [Measure.map_apply hf
          MeasurableSet.univ, Set.preimage_univ]
      _ = _ := by
        simp only [hmap, Measure.smul_apply,
          smul_eq_mul]
  have hscalar :
      (c * ν Set.univ)⁻¹ * c =
        (ν Set.univ)⁻¹ := by
    rw [ENNReal.mul_inv
      (Or.inl hc0) (Or.inl hcT)]
    calc
      _ = (c⁻¹*c)*(ν Set.univ)⁻¹ := by
        ac_rfl
      _ = _ := by
        rw [ENNReal.inv_mul_cancel hc0 hcT,
          one_mul]
  unfold normalized
  rw [Measure.map_smul, hmap, smul_smul,
    hmass, hscalar]

theorem normalized_restriction_transport
    (μ : Measure α) (ν : Measure β)
    (f : α → β) (c : ℝ≥0∞)
    (s : Set α) (t : Set β)
    (hf : Measurable f)
    (ht : MeasurableSet t)
    (hc0 : c ≠ 0)
    (hcT : c ≠ ∞)
    (hpre : f ⁻¹' t = s)
    (hmap : μ.map f = c • ν) :
    (normalized (μ.restrict s)).map f =
      normalized (ν.restrict t) := by
  have h :
      (μ.restrict s).map f =
        c • ν.restrict t := by
    calc
      _ = (μ.map f).restrict t := by
        rw [Measure.restrict_map hf ht, hpre]
      _ = _ := by
        rw [hmap, Measure.restrict_smul]
  exact normalized_map
    (μ.restrict s) (ν.restrict t)
    f c hf hc0 hcT h

theorem pair_event_transport
    (μ : Measure α) (ν : Measure β)
    [SFinite μ]
    (f : α → β)
    (A : Set (α × α))
    (B : Set (β × β))
    (hf : Measurable f)
    (hB : MeasurableSet B)
    (hmap : μ.map f = ν)
    (hpre : (Prod.map f f) ⁻¹' B = A) :
    (ν.prod ν) B = (μ.prod μ) A := by
  rw [← hmap, Measure.map_prod_map μ μ hf hf,
    Measure.map_apply (hf.prodMap hf) hB, hpre]

theorem restriction_mass
    (μ ν : Measure α)
    (D : Set α)
    (J : ℝ≥0∞)
    (hν : ν Set.univ = 1)
    (hrestrict : μ.restrict D = J • ν) :
    μ D = J := by
  have h := congrArg
    (fun τ : Measure α => τ Set.univ) hrestrict
  simpa [Measure.restrict_apply,
    Measure.smul_apply, smul_eq_mul, hν] using h

theorem restricted_pair_mass
    (μ ν : Measure α)
    [SFinite μ] [SFinite ν]
    (D : Set α)
    (B : Set (α × α))
    (J : ℝ≥0∞)
    (hB : MeasurableSet B)
    (hrestrict : μ.restrict D = J • ν) :
    (μ.prod μ) (B ∩ (D ×ˢ D)) =
      J * J * (ν.prod ν) B := by
  calc
    _ = ((μ.prod μ).restrict (D ×ˢ D)) B :=
      (Measure.restrict_apply hB).symm
    _ = ((μ.restrict D).prod
          (μ.restrict D)) B := by
      rw [Measure.prod_restrict]
    _ = _ := by
      rw [hrestrict, Measure.prod_smul_left,
        Measure.prod_smul_right]
      simp only [Measure.smul_apply,
        smul_eq_mul, mul_assoc]

theorem future_pair_mass
    (μ ν : Measure α)
    [SFinite μ] [SFinite ν]
    (D : Set α)
    (B : Set (α × α))
    (f : α → α)
    (J : ℝ≥0∞)
    (hf : Measurable f)
    (hB : MeasurableSet B)
    (hν : ν Set.univ = 1)
    (hmap : μ.map f = ν)
    (hpre : (Prod.map f f) ⁻¹' B = B)
    (hrestrict : μ.restrict D = J • ν) :
    (μ.prod μ) (B ∩ (D ×ˢ D)) =
      (μ D) * (μ D) * (μ.prod μ) B := by
  have hJ := restriction_mass μ ν D J hν hrestrict
  have hp :=
    pair_event_transport μ ν f B B
      hf hB hmap hpre
  rw [restricted_pair_mass μ ν D B J hB hrestrict,
    hp, hJ]

#print axioms normalized_map
#print axioms normalized_restriction_transport
#print axioms pair_event_transport
#print axioms restriction_mass
#print axioms restricted_pair_mass
#print axioms future_pair_mass

end Chronos.GeometricTransport


open scoped InnerProductSpace

namespace Chronos.MinkowskiSimilarity

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [InnerProductSpace ℝ E]

noncomputable def boostTime
    (w : E) (t : ℝ) (x : E) : ℝ :=
  (1+‖w‖^2)*t + 2*⟪w,x⟫_ℝ

noncomputable def boostSpace
    (w : E) (t : ℝ) (x : E) : E :=
  (1-‖w‖^2) • x +
    (2*(t+⟪w,x⟫_ℝ)) • w

theorem lorentz_square
    (w : E) (t : ℝ) (x : E) :
    (boostTime w t x)^2 -
      ‖boostSpace w t x‖^2 =
    (1-‖w‖^2)^2 *
      (t^2-‖x‖^2) := by
  rw [← real_inner_self_eq_norm_sq
    (boostSpace w t x),
    ← real_inner_self_eq_norm_sq x]
  simp only [
    boostTime, boostSpace,
    inner_add_left, inner_add_right,
    real_inner_smul_left,
    real_inner_smul_right,
    real_inner_self_eq_norm_sq,
    real_inner_comm x w]
  simp only [norm_smul, Real.norm_eq_abs,
    mul_pow, sq_abs]
  ring

omit [InnerProductSpace ℝ E] in
theorem q_pos_of_future
    (t : ℝ) (x : E)
    (h : ‖x‖ < t) :
    0 < t^2-‖x‖^2 := by
  have hsum : 0 < t+‖x‖ := by
    linarith [norm_nonneg x]
  have hm := mul_pos
    (sub_pos.mpr h) hsum
  nlinarith only [hm]

omit [InnerProductSpace ℝ E] in
theorem future_of_q_pos
    (t : ℝ) (x : E)
    (ht : 0 < t)
    (hq : 0 < t^2-‖x‖^2) :
    ‖x‖ < t := by
  by_contra! h
  have hm := mul_nonneg
    (sub_nonneg.mpr h)
    (show 0 ≤ ‖x‖+t by
      linarith [norm_nonneg x])
  nlinarith only [hm,hq]

theorem boost_time_positive
    (w : E) (t : ℝ) (x : E)
    (hw : ‖w‖ < 1)
    (hx : ‖x‖ < t) :
    0 < boostTime w t x := by
  have ht : 0 < t :=
    lt_of_le_of_lt (norm_nonneg x) hx
  have hi :
      -(‖w‖*‖x‖) ≤ ⟪w,x⟫_ℝ :=
    (abs_le.mp
      (abs_real_inner_le_norm w x)).1
  have hm := mul_nonneg
    (norm_nonneg w)
    (sub_nonneg.mpr hx.le)
  have hp := mul_pos
    (pow_pos (sub_pos.mpr hw) 2) ht
  unfold boostTime
  nlinarith only [hi,hm,hp]

theorem future_iff
    (w : E) (t : ℝ) (x : E)
    (hw : ‖w‖ < 1) :
    ‖boostSpace w t x‖ <
      boostTime w t x ↔ ‖x‖ < t := by
  constructor
  · intro h
    have hq' := q_pos_of_future
      (boostTime w t x)
      (boostSpace w t x) h
    rw [lorentz_square] at hq'
    have hq : 0 < t^2-‖x‖^2 := by
      by_contra! hn
      exact (not_lt_of_ge
        (mul_nonpos_of_nonneg_of_nonpos
          (sq_nonneg (1-‖w‖^2)) hn)) hq'
    have ht : 0 < t := by
      by_contra! hn
      have hnt : 0 < -t := by
        by_contra! hz
        have he : t = 0 := by linarith
        rw [he] at hq
        nlinarith [sq_nonneg ‖x‖]
      have hneg : ‖x‖ < -t :=
        future_of_q_pos (-t) x hnt
          (by nlinarith only [hq])
      have hb := boost_time_positive
        w (-t) (-x) hw
        (by simpa only [norm_neg] using hneg)
      have he :
          boostTime w (-t) (-x) =
            -boostTime w t x := by
        simp only [boostTime, inner_neg_right]
        ring
      rw [he] at hb
      linarith [norm_nonneg (boostSpace w t x)]
    exact future_of_q_pos t x ht hq
  · intro h
    apply future_of_q_pos
    · exact boost_time_positive w t x hw h
    · rw [lorentz_square]
      have hr : 0 < 1-‖w‖^2 := by
        have hm := mul_pos
          (sub_pos.mpr hw)
          (show 0 < 1+‖w‖ by
            linarith [norm_nonneg w])
        nlinarith only [hm]
      exact mul_pos (pow_pos hr 2)
        (q_pos_of_future t x h)

theorem boostTime_sub
    (w : E) (t s : ℝ) (x y : E) :
    boostTime w (t-s) (x-y) =
      boostTime w t x - boostTime w s y := by
  simp only [boostTime, inner_sub_right]
  ring

theorem boostSpace_sub
    (w : E) (t s : ℝ) (x y : E) :
    boostSpace w (t-s) (x-y) =
      boostSpace w t x - boostSpace w s y := by
  simp only [boostSpace, inner_sub_right]
  module

theorem causal_order_iff
    (w : E) (t s : ℝ) (x y : E)
    (hw : ‖w‖ < 1) :
    ‖boostSpace w t x -
      boostSpace w s y‖ <
      boostTime w t x -
      boostTime w s y ↔
    ‖x-y‖ < t-s := by
  rw [← boostSpace_sub, ← boostTime_sub]
  exact future_iff w (t-s) (x-y) hw

theorem inverse_time
    (w : E) (t : ℝ) (x : E) :
    boostTime (-w)
      (boostTime w t x)
      (boostSpace w t x) =
    (1-‖w‖^2)^2*t := by
  simp only [
    boostTime, boostSpace,
    norm_neg, inner_neg_left,
    inner_add_right,
    real_inner_smul_right,
    real_inner_self_eq_norm_sq]
  ring

theorem inverse_space
    (w : E) (t : ℝ) (x : E) :
    boostSpace (-w)
      (boostTime w t x)
      (boostSpace w t x) =
    ((1-‖w‖^2)^2) • x := by
  simp only [
    boostTime, boostSpace,
    norm_neg, inner_neg_left,
    inner_add_right,
    real_inner_smul_right,
    real_inner_self_eq_norm_sq,
    smul_neg]
  module

theorem boostTime_tip (w : E) :
    boostTime w 1 (0:E) = 1+‖w‖^2 := by
  simp [boostTime]

theorem boostSpace_tip (w : E) :
    boostSpace w 1 (0:E) = (2:ℝ) • w := by
  simp [boostSpace]

theorem tip_reachable
    (a : ℝ) (v : E)
    (ha : ‖v‖ < a) :
    ∃ (c : ℝ) (w : E),
      0 < c ∧ ‖w‖ < 1 ∧
      c*boostTime w 1 (0:E) = a ∧
      c • boostSpace w 1 (0:E) = v := by
  let τ := Real.sqrt (a^2-‖v‖^2)
  have hq := q_pos_of_future a v ha
  have hτ : 0 < τ :=
    Real.sqrt_pos.2 hq
  have hτ2 : τ^2 = a^2-‖v‖^2 :=
    Real.sq_sqrt hq.le
  have hs : 0 < a+τ := by
    linarith [norm_nonneg v]
  let w : E := (a+τ)⁻¹ • v
  have hn : ‖w‖ = ‖v‖/(a+τ) := by
    dsimp [w]
    rw [norm_smul, Real.norm_eq_abs,
      abs_of_pos (inv_pos.mpr hs)]
    ring
  have hw : ‖w‖ < 1 := by
    rw [hn]
    apply (div_lt_iff₀ hs).2
    linarith
  have he :
      ‖v‖^2 = (a-τ)*(a+τ) := by
    nlinarith only [hτ2]
  have hnormsq :
      (‖v‖/(a+τ))^2 =
        (a-τ)/(a+τ) := by
    rw [div_pow,he]
    field_simp [ne_of_gt hs]
  refine ⟨(a+τ)/2,w,by linarith,hw,?_,?_⟩
  · rw [boostTime_tip,hn,hnormsq]
    field_simp [ne_of_gt hs]; ring
  · rw [boostSpace_tip]
    dsimp [w]
    rw [smul_smul,smul_smul]
    have hc :
        ((a+τ)/2)*2*(a+τ)⁻¹ = 1 := by
      field_simp [ne_of_gt hs]
    rw [hc,one_smul]

#print axioms lorentz_square
#print axioms future_iff
#print axioms causal_order_iff
#print axioms inverse_time
#print axioms inverse_space
#print axioms tip_reachable

end Chronos.MinkowskiSimilarity

open MeasureTheory Set
open scoped InnerProductSpace ENNReal NNReal

namespace Chronos.MinkowskiDiamond

open Chronos.MinkowskiSimilarity
open Chronos.GeometricTransport

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [InnerProductSpace ℝ E]

noncomputable def B
    (w : E) (p : ℝ × E) : ℝ × E :=
  (boostTime w p.1 p.2,
   boostSpace w p.1 p.2)

theorem B_add
    (w : E) (p q : ℝ × E) :
    B w (p+q) = B w p+B w q := by
  apply Prod.ext
  · change
      boostTime w (p.1+q.1) (p.2+q.2) =
      boostTime w p.1 p.2 +
      boostTime w q.1 q.2
    simp only [boostTime, inner_add_right]
    ring
  · change
      boostSpace w (p.1+q.1) (p.2+q.2) =
      boostSpace w p.1 p.2 +
      boostSpace w q.1 q.2
    simp only [boostSpace, inner_add_right]
    module

theorem B_smul
    (w : E) (c : ℝ) (p : ℝ × E) :
    B w (c • p) = c • B w p := by
  apply Prod.ext
  · change
      boostTime w (c*p.1) (c • p.2) =
      c*boostTime w p.1 p.2
    simp only [boostTime, real_inner_smul_right]
    ring
  · change
      boostSpace w (c*p.1) (c • p.2) =
      c • boostSpace w p.1 p.2
    simp only [boostSpace, real_inner_smul_right]
    module

noncomputable def k (w : E) : ℝ :=
  (1-‖w‖^2)^2

omit [InnerProductSpace ℝ E] in
theorem k_pos (w : E)
    (hw : ‖w‖ < 1) :
    0 < k w := by
  unfold k
  have h := mul_pos
    (sub_pos.mpr hw)
    (show 0 < 1+‖w‖ by
      linarith [norm_nonneg w])
  exact pow_pos (by nlinarith only [h]) 2

theorem B_neg_comp
    (w : E) (p : ℝ × E) :
    B (-w) (B w p) = k w • p := by
  apply Prod.ext
  · exact inverse_time w p.1 p.2
  · exact inverse_space w p.1 p.2

theorem B_comp_neg
    (w : E) (p : ℝ × E) :
    B w (B (-w) p) = k w • p := by
  simpa only [neg_neg, k, norm_neg]
    using B_neg_comp (-w) p

noncomputable def scaledEquiv
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1)
    (hc : 0 < c) :
    (ℝ × E) ≃+ (ℝ × E) := by
  have hk : k w ≠ 0 :=
    ne_of_gt (k_pos w hw)
  have hc0 : c ≠ 0 := ne_of_gt hc
  refine {
    toFun := fun p => c • B w p
    invFun := fun p =>
      (c*k w)⁻¹ • B (-w) p
    left_inv := ?_
    right_inv := ?_
    map_add' := ?_
  }
  · intro p
    change
      (c*k w)⁻¹ • B (-w) (c • B w p) = p
    rw [B_smul, B_neg_comp]
    rw [smul_smul c (k w), smul_smul]
    rw [inv_mul_cancel₀
      (mul_ne_zero hc0 hk), one_smul]
  · intro p
    change
      c • B w ((c*k w)⁻¹ • B (-w) p) = p
    rw [B_smul, B_comp_neg]
    rw [smul_smul (c*k w)⁻¹ (k w),
      smul_smul]
    have h :
        c*((c*k w)⁻¹*k w) = 1 := by
      field_simp [hc0,hk]
    rw [h,one_smul]
  · intro p q
    rw [B_add,smul_add]

theorem continuous_B (w : E) :
    Continuous (B w) := by
  unfold B boostTime boostSpace
  fun_prop

theorem continuous_scaledEquiv
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c) :
    Continuous (scaledEquiv w c hw hc) := by
  change Continuous (fun p : ℝ × E =>
    c • B w p)
  exact continuous_const.smul (continuous_B w)

theorem continuous_scaledEquiv_symm
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c) :
    Continuous (scaledEquiv w c hw hc).symm := by
  change Continuous (fun p : ℝ × E =>
    (c*k w)⁻¹ • B (-w) p)
  exact continuous_const.smul
    (continuous_B (-w))

def precedes (p q : ℝ × E) : Prop :=
  ‖q.2-p.2‖ < q.1-p.1

def diamond (a b : ℝ × E) :
    Set (ℝ × E) :=
  {p | precedes a p ∧ precedes p b}

def tip : ℝ × E := (1,0)

theorem scaled_future_iff
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c)
    (p : ℝ × E) :
    ‖(scaledEquiv w c hw hc p).2‖ <
      (scaledEquiv w c hw hc p).1 ↔
    ‖p.2‖ < p.1 := by
  change
    ‖c • boostSpace w p.1 p.2‖ <
      c*boostTime w p.1 p.2 ↔
    ‖p.2‖ < p.1
  rw [norm_smul, Real.norm_eq_abs,
    abs_of_pos hc]
  constructor
  · intro h
    apply (future_iff w p.1 p.2 hw).mp
    by_contra! hn
    have hm := mul_nonneg hc.le
      (sub_nonneg.mpr hn)
    nlinarith only [hm,h]
  · intro h
    have h' := (future_iff w p.1 p.2 hw).mpr h
    have hm := mul_pos hc
      (sub_pos.mpr h')
    nlinarith only [hm]

theorem affine_precedes_iff
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c)
    (a p q : ℝ × E) :
    precedes
      (scaledEquiv w c hw hc p+a)
      (scaledEquiv w c hw hc q+a) ↔
    precedes p q := by
  let e := scaledEquiv w c hw hc
  have h :
      (e q+a)-(e p+a) = e (q-p) := by
    rw [map_sub]
    abel
  change
    ‖((e q+a)-(e p+a)).2‖ <
      ((e q+a)-(e p+a)).1 ↔
    ‖(q-p).2‖ < (q-p).1
  rw [h]
  exact scaled_future_iff w c hw hc (q-p)

omit [InnerProductSpace ℝ E] in
theorem diamond_open (a b : ℝ × E) :
    IsOpen (diamond a b) := by
  have h1 : Continuous
      (fun p : ℝ × E => ‖p.2-a.2‖) := by
    fun_prop
  have h2 : Continuous
      (fun p : ℝ × E => p.1-a.1) := by
    fun_prop
  have h3 : Continuous
      (fun p : ℝ × E => ‖b.2-p.2‖) := by
    fun_prop
  have h4 : Continuous
      (fun p : ℝ × E => b.1-p.1) := by
    fun_prop
  change IsOpen
    ({p : ℝ × E | ‖p.2-a.2‖ < p.1-a.1} ∩
     {p : ℝ × E | ‖b.2-p.2‖ < b.1-p.1})
  exact (isOpen_lt h1 h2).inter
    (isOpen_lt h3 h4)

section Haar

variable [MeasurableSpace E] [BorelSpace E]
variable [SecondCountableTopology E]
variable [LocallyCompactSpace E]

omit [InnerProductSpace ℝ E] in
theorem affine_haar_scaling
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (e : (ℝ × E) ≃+ (ℝ × E))
    (he : Continuous e)
    (hei : Continuous e.symm)
    (a : ℝ × E) :
    ∃ c : ℝ≥0∞,
      c ≠ 0 ∧ c ≠ ∞ ∧
      μ.map (fun p => e p+a) = c • μ := by
  letI : (μ.map e).IsAddHaarMeasure :=
    e.isAddHaarMeasure_map μ he hei
  let ν := (μ.map e).map (· + a)
  letI : ν.IsAddHaarMeasure := by
    dsimp [ν]
    infer_instance
  let c : ℝ≥0 :=
    Measure.addHaarScalarFactor ν μ
  have hc : 0 < c := by
    apply pos_iff_ne_zero.mpr
    intro H
    change Measure.addHaarScalarFactor ν μ = 0 at H
    have hmul :=
      Measure.addHaarScalarFactor_eq_mul ν μ ν
    simp [H] at hmul
  refine ⟨(c:ℝ≥0∞), ?_, ENNReal.coe_ne_top, ?_⟩
  · exact ENNReal.coe_ne_zero.mpr (ne_of_gt hc)
  · have hm :
        ν = (c:ℝ≥0∞) • μ := by
      exact Measure.isAddLeftInvariant_eq_smul ν μ
    have hmap :
        ν = μ.map (fun p => e p+a) := by
      unfold ν
      have hg : Measurable
          (fun p : ℝ × E => p+a) := by
        fun_prop
      exact Measure.map_map hg he.measurable
    rw [← hmap]
    exact hm

theorem diamond_transport
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    ∃ f : (ℝ × E) → (ℝ × E),
      Measurable f ∧
      Function.Bijective f ∧
      f 0 = a ∧
      f tip = b ∧
      (∀ p q, precedes (f p) (f q) ↔ precedes p q) ∧
      f ⁻¹' diamond a b = diamond 0 tip ∧
      (normalized
        (μ.restrict (diamond 0 tip))).map f =
      normalized (μ.restrict (diamond a b)) := by
  obtain ⟨c,w,hc,hw,ht,hs⟩ :=
    tip_reachable (b.1-a.1) (b.2-a.2) hab
  let e := scaledEquiv w c hw hc
  let f : (ℝ × E) → (ℝ × E) :=
    fun p => e p+a
  have he : Continuous e :=
    continuous_scaledEquiv w c hw hc
  have hei : Continuous e.symm :=
    continuous_scaledEquiv_symm w c hw hc
  have hf : Measurable f :=
    (he.add continuous_const).measurable
  have h0 : f 0 = a := by
    simp [f]
  have htip : f tip = b := by
    apply Prod.ext
    · change c*boostTime w 1 (0:E)+a.1 = b.1
      rw [ht]
      ring
    · change
        c • boostSpace w 1 (0:E)+a.2 = b.2
      rw [hs]
      abel
  have horder :
      ∀ p q, precedes (f p) (f q) ↔
        precedes p q :=
    fun p q => affine_precedes_iff
      w c hw hc a p q
  have hpre :
      f ⁻¹' diamond a b = diamond 0 tip := by
    ext p
    change
      (precedes a (f p) ∧ precedes (f p) b) ↔
      (precedes 0 p ∧ precedes p tip)
    rw [← h0, ← htip, horder, horder]
  have hbij : Function.Bijective f := by
    constructor
    · intro p q hpq
      apply e.injective
      exact add_right_cancel hpq
    · intro q
      refine ⟨e.symm (q-a), ?_⟩
      change e (e.symm (q-a))+a = q
      rw [e.apply_symm_apply]
      abel
  obtain ⟨s,hs0,hsT,hmap⟩ :=
    affine_haar_scaling μ e he hei a
  refine ⟨f,hf,hbij,h0,htip,horder,hpre,?_⟩
  exact normalized_restriction_transport
    μ μ f s (diamond 0 tip) (diamond a b)
    hf (diamond_open a b).measurableSet
    hs0 hsT hpre hmap

end Haar

#print axioms B_add
#print axioms B_smul
#print axioms B_neg_comp
#print axioms scaledEquiv
#print axioms affine_precedes_iff
#print axioms affine_haar_scaling
#print axioms diamond_transport

end Chronos.MinkowskiDiamond

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.MinkowskiProbability

open Chronos.MinkowskiDiamond
open Chronos.GeometricTransport

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [InnerProductSpace ℝ E]
variable [MeasurableSpace E] [BorelSpace E]
variable [SecondCountableTopology E]
variable [ProperSpace E]
variable [LocallyCompactSpace E]

noncomputable def uniform
    (μ : Measure (ℝ × E))
    (a b : ℝ × E) :
    Measure (ℝ × E) :=
  normalized (μ.restrict (diamond a b))

def comparable :
    Set ((ℝ × E) × (ℝ × E)) :=
  {z | precedes z.1 z.2 ∨
       precedes z.2 z.1}

omit [InnerProductSpace ℝ E] [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] [ProperSpace E] [LocallyCompactSpace E] in
theorem comparable_open :
    IsOpen (comparable (E := E)) := by
  have h1 : Continuous
      (fun z : (ℝ × E) × (ℝ × E) =>
        ‖z.2.2-z.1.2‖) := by
    fun_prop
  have h2 : Continuous
      (fun z : (ℝ × E) × (ℝ × E) =>
        z.2.1-z.1.1) := by
    fun_prop
  have h3 : Continuous
      (fun z : (ℝ × E) × (ℝ × E) =>
        ‖z.1.2-z.2.2‖) := by
    fun_prop
  have h4 : Continuous
      (fun z : (ℝ × E) × (ℝ × E) =>
        z.1.1-z.2.1) := by
    fun_prop
  exact (isOpen_lt h1 h2).union
    (isOpen_lt h3 h4)

omit [InnerProductSpace ℝ E] [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] [ProperSpace E] [LocallyCompactSpace E] in
theorem canonical_nonempty :
    (diamond (0:ℝ × E) tip).Nonempty := by
  refine ⟨((1/2:ℝ),(0:E)),?_⟩
  change
    ‖(0:E)-0‖ < (1/2:ℝ)-0 ∧
    ‖(0:E)-0‖ < 1-(1/2:ℝ)
  norm_num

omit [ProperSpace E] in
theorem diamond_nonempty
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    (diamond a b).Nonempty := by
  obtain ⟨f,_,_,_,_,_,hpre,_⟩ :=
    diamond_transport μ a b hab
  obtain ⟨p,hp⟩ :=
    canonical_nonempty (E := E)
  refine ⟨f p,?_⟩
  change p ∈ f ⁻¹' diamond a b
  rw [hpre]
  exact hp

omit [InnerProductSpace ℝ E] [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] [ProperSpace E] [LocallyCompactSpace E] in
theorem diamond_bounded
    (a b : ℝ × E) :
    diamond a b ⊆
      Metric.closedBall a (b.1-a.1) := by
  intro p hp
  change
    ‖p.2-a.2‖ < p.1-a.1 ∧
    ‖b.2-p.2‖ < b.1-p.1 at hp
  have hpa : 0 ≤ p.1-a.1 := by
    linarith [norm_nonneg (p.2-a.2)]
  have hpb : p.1 ≤ b.1 := by
    linarith [norm_nonneg (b.2-p.2)]
  rw [Metric.mem_closedBall,
    dist_eq_norm, Prod.norm_def]
  have ht :
      ‖p.1-a.1‖ ≤ b.1-a.1 := by
    rw [Real.norm_eq_abs,
      abs_of_nonneg hpa]
    linarith
  have hx :
      ‖p.2-a.2‖ ≤ b.1-a.1 := by
    linarith [hp.1]
  exact max_le ht hx

theorem diamond_volume_bounds
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    0 < μ (diamond a b) ∧
    μ (diamond a b) < ∞ := by
  constructor
  · exact IsOpen.measure_pos μ
      (diamond_open a b)
      (diamond_nonempty μ a b hab)
  · exact lt_of_le_of_lt
      (measure_mono (diamond_bounded a b))
      (isCompact_closedBall
        a (b.1-a.1)).measure_lt_top

theorem uniform_probability
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    IsProbabilityMeasure (uniform μ a b) := by
  have h := diamond_volume_bounds μ a b hab
  have hmass :
      (μ.restrict (diamond a b)) Set.univ =
      μ (diamond a b) := by
    simp
  constructor
  unfold uniform normalized
  rw [Measure.smul_apply, smul_eq_mul,
    hmass, ENNReal.inv_mul_cancel
      (ne_of_gt h.1) (ne_of_lt h.2)]

omit [InnerProductSpace ℝ E] [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] [ProperSpace E] [LocallyCompactSpace E] in
theorem canonical_timelike :
    precedes (0:ℝ × E) tip := by
  change ‖(0:E)-0‖ < (1:ℝ)-0
  norm_num

omit [InnerProductSpace ℝ E] [MeasurableSpace E] [BorelSpace E] [SecondCountableTopology E] [ProperSpace E] [LocallyCompactSpace E] in
theorem comparable_preimage
    (f : (ℝ × E) → (ℝ × E))
    (horder : ∀ p q,
      precedes (f p) (f q) ↔ precedes p q) :
    (Prod.map f f) ⁻¹' comparable =
      comparable := by
  ext z
  change
    (precedes (f z.1) (f z.2) ∨
     precedes (f z.2) (f z.1)) ↔
    (precedes z.1 z.2 ∨
     precedes z.2 z.1)
  rw [horder,horder]

noncomputable def pairProbability
    (μ : Measure (ℝ × E))
    (a b : ℝ × E) : ℝ≥0∞ :=
  ((uniform μ a b).prod
    (uniform μ a b)) comparable

theorem pair_probability_invariant
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    pairProbability μ a b =
      pairProbability μ 0 tip := by
  obtain ⟨f,hf,_,_,_,horder,_,hmap⟩ :=
    diamond_transport μ a b hab
  letI : IsProbabilityMeasure
      (uniform μ 0 tip) :=
    uniform_probability μ 0 tip
      (canonical_timelike (E := E))
  unfold pairProbability
  exact pair_event_transport
    (uniform μ 0 tip)
    (uniform μ a b)
    f comparable comparable hf
    (comparable_open (E := E)).measurableSet
    hmap
    (comparable_preimage f horder)

theorem arbitrary_diamond_pair_probability
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b c d : ℝ × E)
    (hab : precedes a b)
    (hcd : precedes c d) :
    pairProbability μ a b =
      pairProbability μ c d := by
  rw [pair_probability_invariant μ a b hab,
    pair_probability_invariant μ c d hcd]

#print axioms comparable_open
#print axioms canonical_nonempty
#print axioms diamond_nonempty
#print axioms diamond_bounded
#print axioms diamond_volume_bounds
#print axioms uniform_probability
#print axioms comparable_preimage
#print axioms pair_probability_invariant
#print axioms arbitrary_diamond_pair_probability

end Chronos.MinkowskiProbability

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.MinkowskiVolume

open Chronos.MinkowskiSimilarity
open Chronos.MinkowskiDiamond

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [InnerProductSpace ℝ E]

noncomputable def L (w : E) :
    (ℝ × E) →ₗ[ℝ] (ℝ × E) where
  toFun := B w
  map_add' := B_add w
  map_smul' := B_smul w

def R : (ℝ × E) →ₗ[ℝ] (ℝ × E) where
  toFun := fun p => (p.1,-p.2)
  map_add' := by
    intro p q
    apply Prod.ext <;> simp [add_comm]
  map_smul' := by
    intro c p
    apply Prod.ext <;> simp

theorem reflection_square :
    (R (E := E)).comp R = LinearMap.id := by
  apply LinearMap.ext
  intro p
  change (p.1,-(-p.2)) = p
  simp

theorem boost_reflection (w : E) :
    L (-w) = R.comp ((L w).comp R) := by
  apply LinearMap.ext
  intro p
  apply Prod.ext
  · change
      boostTime (-w) p.1 p.2 =
      boostTime w p.1 (-p.2)
    simp only [boostTime,norm_neg,
      inner_neg_left,inner_neg_right]
  · change
      boostSpace (-w) p.1 p.2 =
      -boostSpace w p.1 (-p.2)
    simp only [boostSpace,norm_neg,
      inner_neg_left,inner_neg_right]
    module

theorem boost_inverse_product (w : E) :
    (L (-w)).comp (L w) =
      k w • LinearMap.id := by
  apply LinearMap.ext
  intro p
  exact B_neg_comp w p

section Determinant

variable [FiniteDimensional ℝ E]

omit [FiniteDimensional ℝ E] in
theorem reflection_det_square :
    LinearMap.det (R (E := E)) *
      LinearMap.det (R (E := E)) = 1 := by
  have h := congrArg
    (fun f : (ℝ × E) →ₗ[ℝ] (ℝ × E) =>
      LinearMap.det f)
    (reflection_square (E := E))
  dsimp only at h
  rw [LinearMap.det_comp,
    LinearMap.det_id] at h
  exact h

omit [FiniteDimensional ℝ E] in
theorem boost_det_neg (w : E) :
    LinearMap.det (L (-w)) =
      LinearMap.det (L w) := by
  calc
    LinearMap.det (L (-w)) =
        (LinearMap.det (R (E := E)) *
          LinearMap.det (R (E := E))) *
          LinearMap.det (L w) := by
      rw [boost_reflection,
        LinearMap.det_comp,
        LinearMap.det_comp]
      ring
    _ = _ := by
      rw [reflection_det_square,one_mul]

omit [FiniteDimensional ℝ E] in
theorem boost_abs_det
    (w : E) (hw : ‖w‖ < 1) :
    |LinearMap.det (L w)| =
      (1-‖w‖^2)^Module.finrank ℝ (ℝ × E) := by
  let n := Module.finrank ℝ (ℝ × E)
  have h := congrArg
    (fun f : (ℝ × E) →ₗ[ℝ] (ℝ × E) =>
      LinearMap.det f)
    (boost_inverse_product w)
  dsimp only at h
  rw [LinearMap.det_comp,
    boost_det_neg,
    LinearMap.det_smul,
    LinearMap.det_id,mul_one] at h
  have hp : 0 < 1-‖w‖^2 := by
    have hm := mul_pos
      (sub_pos.mpr hw)
      (show 0 < 1+‖w‖ by
        linarith [norm_nonneg w])
    nlinarith only [hm]
  have hs :
      LinearMap.det (L w)^2 =
        ((1-‖w‖^2)^n)^2 := by
    calc
      LinearMap.det (L w)^2 =
          (k w)^n := by
        simpa only [pow_two,n] using h
      _ = _ := by
        unfold k
        rw [← pow_mul, ← pow_mul,
          Nat.mul_comm 2 n]
  have ha :=
    (sq_eq_sq_iff_abs_eq_abs _ _).mp hs
  rw [abs_of_nonneg
    (pow_nonneg hp.le n)] at ha
  exact ha

omit [FiniteDimensional ℝ E] in
theorem scaled_boost_abs_det
    (w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c) :
    |LinearMap.det (c • L w)| =
      (c*(1-‖w‖^2))^
        Module.finrank ℝ (ℝ × E) := by
  rw [LinearMap.det_smul,abs_mul,
    abs_pow,abs_of_pos hc,
    boost_abs_det w hw,← mul_pow]

omit [FiniteDimensional ℝ E] in
theorem proper_time_of_tip
    (a : ℝ) (v w : E) (c : ℝ)
    (hw : ‖w‖ < 1) (hc : 0 < c)
    (ht : c*boostTime w 1 0 = a)
    (hs : c • boostSpace w 1 0 = v) :
    Real.sqrt (a^2-‖v‖^2) =
      c*(1-‖w‖^2) := by
  have hp : 0 < 1-‖w‖^2 := by
    have hm := mul_pos
      (sub_pos.mpr hw)
      (show 0 < 1+‖w‖ by
        linarith [norm_nonneg w])
    nlinarith only [hm]
  have hq :
      a^2-‖v‖^2 =
        (c*(1-‖w‖^2))^2 := by
    calc
      a^2-‖v‖^2 =
          (c*boostTime w 1 0)^2 -
            ‖c • boostSpace w 1 0‖^2 := by
        rw [ht,hs]
      _ = c^2 *
          ((boostTime w 1 0)^2 -
            ‖boostSpace w 1 0‖^2) := by
        rw [norm_smul,Real.norm_eq_abs,
          abs_of_pos hc]
        ring
      _ = _ := by
        rw [lorentz_square]
        simp [pow_two]; ring
  rw [hq,Real.sqrt_sq
    (mul_nonneg hc.le hp.le)]

section Haar

variable [MeasurableSpace E] [BorelSpace E]

theorem diamond_volume_scaling
    (μ : Measure (ℝ × E))
    [μ.IsAddHaarMeasure]
    (a b : ℝ × E)
    (hab : precedes a b) :
    μ (diamond a b) =
      ENNReal.ofReal
        ((Real.sqrt
          ((b.1-a.1)^2-‖b.2-a.2‖^2))^
          Module.finrank ℝ (ℝ × E)) *
      μ (diamond 0 tip) := by
  obtain ⟨c,w,hc,hw,ht,hs⟩ :=
    tip_reachable
      (b.1-a.1) (b.2-a.2) hab
  let e := scaledEquiv w c hw hc
  let T : (ℝ × E) →ₗ[ℝ] (ℝ × E) :=
    c • L w
  let f : (ℝ × E) → (ℝ × E) :=
    fun p => T p+a
  have h0 : f 0 = a := by
    simp [f]
  have htip : f tip = b := by
    apply Prod.ext
    · change c*boostTime w 1 0+a.1 = b.1
      rw [ht]
      ring
    · change
        c • boostSpace w 1 0+a.2 = b.2
      rw [hs]
      abel
  have hord :
      ∀ p q, precedes (f p) (f q) ↔
        precedes p q := by
    intro p q
    exact affine_precedes_iff
      w c hw hc a p q
  have hpre :
      f ⁻¹' diamond a b = diamond 0 tip := by
    ext p
    change
      (precedes a (f p) ∧ precedes (f p) b) ↔
      (precedes 0 p ∧ precedes p tip)
    rw [← h0,← htip,hord,hord]
  have hsurj : Function.Surjective f := by
    intro q
    refine ⟨e.symm (q-a),?_⟩
    change e (e.symm (q-a))+a = q
    rw [e.apply_symm_apply]
    abel
  have himage :
      f '' diamond 0 tip = diamond a b := by
    rw [← hpre]
    exact Set.image_preimage_eq _ hsurj
  have htrans :
      f '' diamond 0 tip =
      (fun p : ℝ × E => p + (-a)) ⁻¹'
        (T '' diamond 0 tip) := by
    ext p
    constructor
    · rintro ⟨x,hx,rfl⟩
      change
        (T x+a)+(-a) ∈ T '' diamond 0 tip
      exact ⟨x,hx,by abel⟩
    · intro hp
      change p+(-a) ∈ T '' diamond 0 tip at hp
      obtain ⟨x,hx,hxp⟩ := hp
      refine ⟨x,hx,?_⟩
      change T x+a = p
      rw [hxp]
      abel
  calc
    μ (diamond a b) =
        μ (f '' diamond 0 tip) := by
      rw [himage]
    _ = μ (T '' diamond 0 tip) := by
      rw [htrans,measure_preimage_add_right]
    _ = ENNReal.ofReal
          |LinearMap.det T| *
          μ (diamond 0 tip) :=
      Measure.addHaar_image_linearMap μ T _
    _ = _ := by
      unfold T
      rw [scaled_boost_abs_det w c hw hc,
        ← proper_time_of_tip
          (b.1-a.1) (b.2-a.2) w c hw hc ht hs]

end Haar
end Determinant

#print axioms reflection_square
#print axioms boost_reflection
#print axioms boost_inverse_product
#print axioms reflection_det_square
#print axioms boost_det_neg
#print axioms boost_abs_det
#print axioms scaled_boost_abs_det
#print axioms proper_time_of_tip
#print axioms diamond_volume_scaling

end Chronos.MinkowskiVolume


open MeasureTheory
open scoped Interval

namespace Chronos.RadialMoments

theorem integral_three
    (a b c y : ℝ) (i j k : ℕ) :
    (∫ x in (0:ℝ)..y,
      a*x^i-b*x^j+c*x^k) =
      a*((y^(i+1)-0^(i+1))/(i+1)) -
      b*((y^(j+1)-0^(j+1))/(j+1)) +
      c*((y^(k+1)-0^(k+1))/(k+1)) := by
  have h1 : IntervalIntegrable
      (fun x : ℝ => a*x^i) volume 0 y :=
    (show Continuous
      (fun x : ℝ => a*x^i) by
        fun_prop).intervalIntegrable _ _
  have h2 : IntervalIntegrable
      (fun x : ℝ => b*x^j) volume 0 y :=
    (show Continuous
      (fun x : ℝ => b*x^j) by
        fun_prop).intervalIntegrable _ _
  have h3 : IntervalIntegrable
      (fun x : ℝ => c*x^k) volume 0 y :=
    (show Continuous
      (fun x : ℝ => c*x^k) by
        fun_prop).intervalIntegrable _ _
  rw [intervalIntegral.integral_add
      (h1.sub h2) h3,
    intervalIntegral.integral_sub h1 h2]
  simp only [
    intervalIntegral.integral_const_mul,
    integral_pow]

noncomputable def inner
    (k : ℕ) (y : ℝ) : ℝ :=
  ∫ x in (0:ℝ)..y,
    (y-x)^2*(x*y)^k

theorem inner_formula
    (k : ℕ) (y : ℝ) :
    inner k y =
      y^(k+2) *
        ((y^(k+1)-0^(k+1))/(k+1)) -
      (2*y^(k+1)) *
        ((y^((k+1)+1)-0^((k+1)+1))/
          ((k+1)+1)) +
      y^k *
        ((y^((k+2)+1)-0^((k+2)+1))/
          ((k+2)+1)) := by
  unfold inner
  calc
    (∫ x in (0:ℝ)..y,
      (y-x)^2*(x*y)^k) =
        ∫ x in (0:ℝ)..y,
          y^(k+2)*x^k -
          (2*y^(k+1))*x^(k+1) +
          y^k*x^(k+2) := by
      apply intervalIntegral.integral_congr
      intro x _
      dsimp only
      rw [mul_pow,
        pow_add y k 2,
        pow_add y k 1,
        pow_add x k 1,
        pow_add x k 2]
      ring
    _ = _ := by
      simpa only [Nat.cast_add, Nat.cast_one,
        Nat.cast_ofNat] using
        integral_three
          (y^(k+2))
          (2*y^(k+1))
          (y^k) y k (k+1) (k+2)

theorem inner_zero (y : ℝ) :
    inner 0 y = y^3/3 := by
  rw [inner_formula]
  norm_num
  ring

theorem inner_two (y : ℝ) :
    inner 2 y = y^7/30 := by
  rw [inner_formula]
  norm_num
  ring

theorem inner_four (y : ℝ) :
    inner 4 y = y^11/105 := by
  rw [inner_formula]
  norm_num
  ring

noncomputable def reducedMoment
    (s : ℕ) : ℝ :=
  12 * ∫ y in (0:ℝ)..1,
    inner (2*s) y

theorem moment_zero :
    reducedMoment 0 = 1 := by
  unfold reducedMoment
  change (12 * ∫ y in (0:ℝ)..1,
    inner 0 y) = 1
  simp_rw [inner_zero]
  rw [intervalIntegral.integral_div,
    integral_pow]
  norm_num

theorem moment_one :
    reducedMoment 1 = 1/20 := by
  unfold reducedMoment
  change (12 * ∫ y in (0:ℝ)..1,
    inner 2 y) = 1/20
  simp_rw [inner_two]
  rw [intervalIntegral.integral_div,
    integral_pow]
  norm_num

theorem moment_two :
    reducedMoment 2 = 1/105 := by
  unfold reducedMoment
  change (12 * ∫ y in (0:ℝ)..1,
    inner 4 y) = 1/105
  simp_rw [inner_four]
  rw [intervalIntegral.integral_div,
    integral_pow]
  norm_num

#print axioms integral_three
#print axioms inner_formula
#print axioms inner_zero
#print axioms inner_two
#print axioms inner_four
#print axioms moment_zero
#print axioms moment_one
#print axioms moment_two

end Chronos.RadialMoments


open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.RadialMeasure

noncomputable def density (r : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (3*r^2)

theorem density_interval
    (b : ℝ) (hb : 0 ≤ b) :
    (∫⁻ r in Ioc 0 b, density r ∂volume) =
      ENNReal.ofReal (b^3) := by
  have hi : IntervalIntegrable
      (fun r : ℝ => 3*r^2) volume 0 b :=
    (show Continuous
      (fun r : ℝ => 3*r^2) by
        fun_prop).intervalIntegrable _ _
  have hn :
      0 ≤ᵐ[volume.restrict (Ioc 0 b)]
        (fun r : ℝ => 3*r^2) :=
    Filter.Eventually.of_forall
      (fun r => by positivity)
  unfold density
  rw [← ofReal_integral_eq_lintegral_ofReal hi.1 hn]
  rw [← intervalIntegral.integral_of_le hb]
  have he :
      (∫ r in (0:ℝ)..b, 3*r^2) = b^3 := by
    rw [intervalIntegral.integral_const_mul,
      integral_pow]
    ring
  rw [he]

section Spatial

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [NormedSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E]
variable [BorelSpace E]

theorem radial_pushforward
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (μ.restrict
      (Metric.closedBall (0:E) 1)).map
        (fun x => ‖x‖) =
      μ (Metric.closedBall (0:E) 1) •
        ((volume.restrict (Ioc (0:ℝ) 1)).withDensity
          density) := by
  have hn : Measurable
      (fun x : E => ‖x‖) :=
    continuous_norm.measurable
  letI : IsFiniteMeasure
      (μ.restrict (Metric.closedBall (0:E) 1)) :=
    isFiniteMeasure_restrict.mpr
      (isCompact_closedBall
        (0:E) 1).measure_lt_top.ne
  letI : IsFiniteMeasure
      ((μ.restrict
        (Metric.closedBall (0:E) 1)).map
          (fun x => ‖x‖)) :=
    Measure.isFiniteMeasure_map _ _
  apply Measure.ext_of_Iic
  intro r
  rw [Measure.map_apply hn measurableSet_Iic,
    Measure.restrict_apply
      (hn measurableSet_Iic),
    Measure.smul_apply,
    smul_eq_mul,
    withDensity_apply _ measurableSet_Iic,
    Measure.restrict_restrict measurableSet_Iic]
  by_cases hr : 0 ≤ r
  · let b := min r 1
    have hb : 0 ≤ b :=
      le_min hr zero_le_one
    have hleft :
        (fun x : E => ‖x‖) ⁻¹' Iic r ∩
          Metric.closedBall (0:E) 1 =
        Metric.closedBall (0:E) b := by
      ext x
      simp only [mem_inter_iff,
        mem_preimage,mem_Iic,
        Metric.mem_closedBall,
        dist_zero_right,b,le_min_iff]
    have hright :
        Iic r ∩ Ioc (0:ℝ) 1 =
        Ioc 0 b := by
      ext x
      simp only [mem_inter_iff,
        mem_Iic,mem_Ioc,b,le_min_iff]
      tauto
    simp only [hleft,hright,
      density_interval b hb,
      Measure.addHaar_closedBall' μ (0:E) hb,
      hdim,mul_comm]
  · have hleft :
        (fun x : E => ‖x‖) ⁻¹' Iic r ∩
          Metric.closedBall (0:E) 1 =
        ∅ := by
      ext x
      simp only [mem_inter_iff,
        mem_preimage,mem_Iic,
        mem_empty_iff_false]
      constructor
      · intro hx
        exact hr
          (le_trans (norm_nonneg x) hx.1)
      · intro h
        exact h.elim
    have hright :
        Iic r ∩ Ioc (0:ℝ) 1 = ∅ := by
      ext x
      simp only [mem_inter_iff,
        mem_Iic,mem_Ioc,
        mem_empty_iff_false]
      constructor
      · intro hx
        exact hr (le_trans hx.2.1.le hx.1)
      · intro h
        exact h.elim
    rw [hleft,hright]
    simp

end Spatial

#print axioms density_interval
#print axioms radial_pushforward

end Chronos.RadialMeasure

open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.PhysicalMoments

open Chronos.MinkowskiDiamond
open Chronos.RadialMeasure

variable {E : Type*}
variable [NormedAddCommGroup E]

def radialMap (p : ℝ × E) : ℝ × ℝ :=
  (p.1,‖p.2‖)

def region : Set (ℝ × ℝ) :=
  {p | p.2 < p.1 ∧ p.2 < 1-p.1}

theorem radialMap_measurable
    [MeasurableSpace E] [BorelSpace E] :
    Measurable (radialMap (E := E)) := by
  unfold radialMap
  fun_prop

theorem region_open :
    IsOpen region := by
  have h1 : Continuous
      (fun p : ℝ × ℝ => p.2) :=
    continuous_snd
  have h2 : Continuous
      (fun p : ℝ × ℝ => p.1) :=
    continuous_fst
  have h3 : Continuous
      (fun p : ℝ × ℝ => 1-p.1) := by
    fun_prop
  exact (isOpen_lt h1 h2).inter
    (isOpen_lt h1 h3)

theorem radial_preimage :
    (radialMap (E := E)) ⁻¹' region =
      diamond (0:ℝ × E) tip := by
  ext p
  change
    (‖p.2‖ < p.1 ∧
     ‖p.2‖ < 1-p.1) ↔
    (‖p.2-0‖ < p.1-0 ∧
     ‖(0:E)-p.2‖ < 1-p.1)
  simp

theorem diamond_in_cylinder :
    diamond (0:ℝ × E) tip ⊆
      (Set.univ : Set ℝ) ×ˢ
        Metric.closedBall (0:E) 1 := by
  intro p hp
  change
    ‖p.2-0‖ < p.1-0 ∧
    ‖(0:E)-p.2‖ < 1-p.1 at hp
  simp only [sub_zero,zero_sub,norm_neg] at hp
  refine ⟨Set.mem_univ _,?_⟩
  rw [Metric.mem_closedBall,
    dist_zero_right]
  linarith [hp.1,hp.2]

noncomputable def radialLaw : Measure ℝ :=
  (volume.restrict (Ioc (0:ℝ) 1)).withDensity
    Chronos.RadialMeasure.density

section Haar

variable [NormedSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E] [BorelSpace E]

theorem cylinder_pushforward
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (((volume : Measure ℝ).prod μ).restrict
      ((Set.univ : Set ℝ) ×ˢ
        Metric.closedBall (0:E) 1)).map
          radialMap =
      μ (Metric.closedBall (0:E) 1) •
        ((volume : Measure ℝ).prod radialLaw) := by
  have hn : Measurable
      (fun x : E => ‖x‖) :=
    continuous_norm.measurable
  have hr :=
    radial_pushforward μ hdim
  have hmap :=
    Measure.map_prod_map
      (volume : Measure ℝ)
      (μ.restrict
        (Metric.closedBall (0:E) 1))
      measurable_id hn
  rw [Measure.map_id] at hmap
  change
    (volume : Measure ℝ).prod
      ((μ.restrict
        (Metric.closedBall (0:E) 1)).map
          (fun x : E => ‖x‖)) =
      ((volume : Measure ℝ).prod
        (μ.restrict
          (Metric.closedBall (0:E) 1))).map
            radialMap at hmap
  rw [hr] at hmap
  change
    (volume : Measure ℝ).prod
      (μ (Metric.closedBall (0:E) 1) •
        radialLaw) = _ at hmap
  letI : IsFiniteMeasure radialLaw :=
    ⟨by
      unfold radialLaw
      rw [withDensity_apply _ MeasurableSet.univ,
        Measure.restrict_univ,
        density_interval 1 zero_le_one]
      norm_num⟩
  rw [Measure.prod_smul_right] at hmap
  have hp :=
    Measure.prod_restrict
      (μ := (volume : Measure ℝ))
      (ν := μ)
      Set.univ
      (Metric.closedBall (0:E) 1)
  rw [Measure.restrict_univ] at hp
  rw [← hp]
  exact hmap.symm

theorem diamond_radial_pushforward
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (((volume : Measure ℝ).prod μ).restrict
      (diamond (0:ℝ × E) tip)).map
        radialMap =
      (μ (Metric.closedBall (0:E) 1) •
        ((volume : Measure ℝ).prod
          radialLaw)).restrict region := by
  let ν := (volume : Measure ℝ).prod μ
  let S :=
    (Set.univ : Set ℝ) ×ˢ
      Metric.closedBall (0:E) 1
  let D := diamond (0:ℝ × E) tip
  have hsub : D ⊆ S :=
    diamond_in_cylinder
  have hpre :
      radialMap ⁻¹' region = D :=
    radial_preimage
  have hr :
      (ν.restrict S).map radialMap =
        μ (Metric.closedBall (0:E) 1) •
          ((volume : Measure ℝ).prod
            radialLaw) :=
    cylinder_pushforward μ hdim
  have hf :=
    radialMap_measurable (E := E)
  change (ν.restrict D).map radialMap = _
  calc
    (ν.restrict D).map radialMap =
        ((ν.restrict S).restrict D).map
          radialMap := by
      rw [Measure.restrict_restrict_of_subset
        hsub]
    _ = ((ν.restrict S).map
          radialMap).restrict region := by
      rw [Measure.restrict_map hf
        region_open.measurableSet,hpre]
    _ = _ := by rw [hr]

theorem physical_radial_integral
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (g : ℝ × ℝ → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p in diamond (0:ℝ × E) tip,
      g (radialMap p)
        ∂((volume : Measure ℝ).prod μ)) =
      μ (Metric.closedBall (0:E) 1) *
      (∫⁻ z in region,
        g z ∂((volume : Measure ℝ).prod
          radialLaw)) := by
  calc
    _ =
      ∫⁻ z, g z ∂
        ((((volume : Measure ℝ).prod μ).restrict
          (diamond (0:ℝ × E) tip)).map
            radialMap) :=
      (lintegral_map hg
        (radialMap_measurable (E := E))).symm
    _ = _ := by
      rw [diamond_radial_pushforward μ hdim,
        Measure.restrict_smul,
        lintegral_smul_measure,smul_eq_mul]

noncomputable def radialWeight
    (s : ℕ) (z : ℝ × ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal
    (((1-z.1)^2-z.2^2)^(2*s))

theorem radialWeight_measurable (s : ℕ) :
    Measurable (radialWeight s) := by
  unfold radialWeight
  apply Measurable.ennreal_ofReal
  fun_prop

theorem physical_moment_radial_reduction
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (s : ℕ) :
    (∫⁻ p in diamond (0:ℝ × E) tip,
      ENNReal.ofReal
        (((1-p.1)^2-‖p.2‖^2)^(2*s))
        ∂((volume : Measure ℝ).prod μ)) =
      μ (Metric.closedBall (0:E) 1) *
      (∫⁻ z in region,
        radialWeight s z
        ∂((volume : Measure ℝ).prod
          radialLaw)) :=
  physical_radial_integral μ hdim
    (radialWeight s)
    (radialWeight_measurable s)

end Haar

#print axioms radialMap_measurable
#print axioms region_open
#print axioms radial_preimage
#print axioms diamond_in_cylinder
#print axioms cylinder_pushforward
#print axioms diamond_radial_pushforward
#print axioms physical_radial_integral
#print axioms radialWeight_measurable
#print axioms physical_moment_radial_reduction

end Chronos.PhysicalMoments

open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.NullCoordinates

open Chronos.PhysicalMoments

abbrev Plane := ℝ × ℝ

def nullLinear : Plane →ₗ[ℝ] Plane where
  toFun := fun p =>
    (-p.1-p.2,-p.1+p.2)
  map_add' := by
    intro p q
    apply Prod.ext
    · change
        -(p.1+q.1)-(p.2+q.2) =
        (-p.1-p.2)+(-q.1-q.2)
      ring
    · change
        -(p.1+q.1)+(p.2+q.2) =
        (-p.1+p.2)+(-q.1+q.2)
      ring
  map_smul' := by
    intro c p
    apply Prod.ext
    · change
        -(c*p.1)-c*p.2 =
          c*(-p.1-p.2)
      ring
    · change
        -(c*p.1)+c*p.2 =
          c*(-p.1+p.2)
      ring

theorem nullLinear_square :
    nullLinear.comp nullLinear =
      (2:ℝ) • LinearMap.id := by
  apply LinearMap.ext
  intro p
  apply Prod.ext
  · change
      -(-p.1-p.2)-(-p.1+p.2) =
        2*p.1
    ring
  · change
      -(-p.1-p.2)+(-p.1+p.2) =
        2*p.2
    ring

theorem nullLinear_abs_det :
    |LinearMap.det nullLinear| = 2 := by
  have h := congrArg
    (fun f : Plane →ₗ[ℝ] Plane =>
      LinearMap.det f)
    nullLinear_square
  dsimp only at h
  rw [LinearMap.det_comp,
    LinearMap.det_smul,
    LinearMap.det_id,
    mul_one] at h
  have hn :
      Module.finrank ℝ Plane = 2 := by
    simp [Plane,Module.finrank_prod]
  rw [hn] at h
  have hs :
      LinearMap.det nullLinear ^ 2 =
        (2:ℝ)^2 := by
    simpa only [pow_two] using h
  have ha :=
    (sq_eq_sq_iff_abs_eq_abs _ _).mp hs
  simpa using ha

def nullMap (p : Plane) : Plane :=
  (1-p.1-p.2,1-p.1+p.2)

noncomputable def nullInverse (p : Plane) : Plane :=
  (1-(p.1+p.2)/2,(p.2-p.1)/2)

theorem null_left_inverse (p : Plane) :
    nullInverse (nullMap p) = p := by
  apply Prod.ext
  · change
      1-((1-p.1-p.2)+(1-p.1+p.2))/2 =
        p.1
    ring
  · change
      ((1-p.1+p.2)-(1-p.1-p.2))/2 =
        p.2
    ring

theorem null_right_inverse (p : Plane) :
    nullMap (nullInverse p) = p := by
  apply Prod.ext
  · change
      1-(1-(p.1+p.2)/2)-(p.2-p.1)/2 =
        p.1
    ring
  · change
      1-(1-(p.1+p.2)/2)+(p.2-p.1)/2 =
        p.2
    ring

theorem nullMap_measurable :
    Measurable nullMap := by
  unfold nullMap
  fun_prop

def triangle : Set Plane :=
  {p | 0 < p.1 ∧ p.1 < p.2 ∧ p.2 < 1}

def sourceRegion : Set Plane :=
  region ∩
    ((Set.univ : Set ℝ) ×ˢ Ioc (0:ℝ) 1)

theorem triangle_measurable :
    MeasurableSet triangle := by
  have h0 : Continuous
      (fun _ : Plane => (0:ℝ)) :=
    continuous_const
  have h1 : Continuous
      (fun p : Plane => p.1) :=
    continuous_fst
  have h2 : Continuous
      (fun p : Plane => p.2) :=
    continuous_snd
  have h3 : Continuous
      (fun _ : Plane => (1:ℝ)) :=
    continuous_const
  exact ((isOpen_lt h0 h1).inter
    ((isOpen_lt h1 h2).inter
      (isOpen_lt h2 h3))).measurableSet

theorem null_preimage :
    nullMap ⁻¹' triangle = sourceRegion := by
  ext p
  change
    (0 < 1-p.1-p.2 ∧
      1-p.1-p.2 < 1-p.1+p.2 ∧
      1-p.1+p.2 < 1) ↔
    ((p.2 < p.1 ∧ p.2 < 1-p.1) ∧
      p.1 ∈ (Set.univ : Set ℝ) ∧
      0 < p.2 ∧ p.2 ≤ 1)
  constructor
  · rintro ⟨h1,h2,h3⟩
    exact ⟨⟨by linarith,by linarith⟩,
      Set.mem_univ _,
      by linarith,by linarith⟩
  · rintro ⟨⟨h1,h2⟩,_,h3,_⟩
    exact ⟨by linarith,
      by linarith,by linarith⟩

theorem null_map_volume :
    (volume : Measure Plane).map nullMap =
      (ENNReal.ofReal (1/2)) •
        (volume : Measure Plane) := by
  letI : (volume : Measure Plane).IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      (volume : Measure ℝ)).IsAddHaarMeasure
    infer_instance
  have hd : LinearMap.det nullLinear ≠ 0 := by
    intro h
    have ha := nullLinear_abs_det
    rw [h,abs_zero] at ha
    norm_num at ha
  have hL :
      (volume : Measure Plane).map nullLinear =
        ENNReal.ofReal
          |(LinearMap.det nullLinear)⁻¹| •
        (volume : Measure Plane) :=
    Measure.map_linearMap_addHaar_eq_smul_addHaar
      volume hd
  rw [abs_inv,nullLinear_abs_det] at hL
  let shift : Plane → Plane :=
    fun p => p+(1,1)
  have hs : Measurable shift := by
    unfold shift
    fun_prop
  have hl : Measurable
      (nullLinear : Plane → Plane) := by
    change Measurable
      (fun p : Plane =>
        (-p.1-p.2,-p.1+p.2))
    fun_prop
  have ht :
      (volume : Measure Plane).map shift =
        volume := by
    ext s hset
    rw [Measure.map_apply hs hset]
    exact measure_preimage_add_right
      (μ := (volume : Measure Plane))
      (1,1) s
  have he :
      shift ∘ nullLinear = nullMap := by
    funext p
    apply Prod.ext
    · change -p.1-p.2+1 =
        1-p.1-p.2
      ring
    · change -p.1+p.2+1 =
        1-p.1+p.2
      ring
  rw [← he,← Measure.map_map hs hl,
    hL,Measure.map_smul,ht]
  norm_num

theorem null_restricted_volume :
    ((volume : Measure Plane).restrict
      sourceRegion).map nullMap =
      ENNReal.ofReal (1/2) •
        ((volume : Measure Plane).restrict
          triangle) := by
  rw [← null_preimage,
    ← Measure.restrict_map
      nullMap_measurable triangle_measurable,
    null_map_volume,Measure.restrict_smul]

theorem null_change_of_variables
    (g : Plane → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p in sourceRegion,
      g (nullMap p) ∂volume) =
      ENNReal.ofReal (1/2) *
        (∫⁻ z in triangle,g z ∂volume) := by
  calc
    _ =
      ∫⁻ z,g z ∂
        (((volume : Measure Plane).restrict
          sourceRegion).map nullMap) :=
      (lintegral_map hg
        nullMap_measurable).symm
    _ = _ := by
      rw [null_restricted_volume,
        lintegral_smul_measure,smul_eq_mul]

theorem null_proper_time_square (p : Plane) :
    (1-p.1)^2-p.2^2 =
      (nullMap p).1*(nullMap p).2 := by
  change
    (1-p.1)^2-p.2^2 =
      (1-p.1-p.2)*(1-p.1+p.2)
  ring

theorem null_radial_weight (p : Plane) :
    3*p.2^2 =
      (3/4)*((nullMap p).2-
        (nullMap p).1)^2 := by
  change
    3*p.2^2 =
      (3/4)*((1-p.1+p.2)-
        (1-p.1-p.2))^2
  ring

#print axioms nullLinear_square
#print axioms nullLinear_abs_det
#print axioms null_left_inverse
#print axioms null_right_inverse
#print axioms nullMap_measurable
#print axioms triangle_measurable
#print axioms null_preimage
#print axioms null_map_volume
#print axioms null_restricted_volume
#print axioms null_change_of_variables
#print axioms null_proper_time_square
#print axioms null_radial_weight

end Chronos.NullCoordinates

open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.NormalizedMoments

open Chronos.PhysicalMoments
open Chronos.NullCoordinates
open Chronos.RadialMoments
open Chronos.RadialMeasure
open Chronos.MinkowskiDiamond

noncomputable def weight
    (s : ℕ) (p : Plane) : ℝ≥0∞ :=
  ENNReal.ofReal
    ((p.2-p.1)^2*(p.1*p.2)^(2*s))

theorem weight_measurable (s : ℕ) :
    Measurable (weight s) := by
  unfold weight
  apply Measurable.ennreal_ofReal
  fun_prop

theorem polynomial_nonnegative
    (s : ℕ) (x y : ℝ) :
    0 ≤ (y-x)^2*(x*y)^(2*s) := by
  rw [pow_mul (x*y) 2 s]
  positivity

theorem inner_lintegral
    (s : ℕ) (y : ℝ) (hy : 0 ≤ y) :
    (∫⁻ x in Ioo 0 y, weight s (x,y)
      ∂volume) =
      ENNReal.ofReal (Chronos.RadialMoments.inner (2*s) y) := by
  have hi : IntervalIntegrable
      (fun x : ℝ =>
        (y-x)^2*(x*y)^(2*s))
      volume 0 y :=
    (show Continuous
      (fun x : ℝ =>
        (y-x)^2*(x*y)^(2*s)) by
          fun_prop).intervalIntegrable _ _
  have hn :
      0 ≤ᵐ[volume.restrict (Ioc 0 y)]
        (fun x : ℝ =>
          (y-x)^2*(x*y)^(2*s)) :=
    Filter.Eventually.of_forall
      (fun x => polynomial_nonnegative s x y)
  rw [restrict_Ioo_eq_restrict_Ioc]
  change
    (∫⁻ x in Ioc 0 y,
      ENNReal.ofReal
        ((y-x)^2*(x*y)^(2*s)) ∂volume) =
      ENNReal.ofReal (Chronos.RadialMoments.inner (2*s) y)
  rw [← ofReal_integral_eq_lintegral_ofReal
    hi.1 hn,
    ← intervalIntegral.integral_of_le hy]
  rfl

theorem triangle_lintegral
    (s : ℕ) :
    (∫⁻ p in triangle, weight s p ∂volume) =
      ENNReal.ofReal
        (reducedMoment s / 12) := by
  have hf := weight_measurable s
  have he :
      (∫⁻ p in triangle, weight s p ∂volume) =
        ∫⁻ y in Ioo (0:ℝ) 1,
          ENNReal.ofReal
            (Chronos.RadialMoments.inner (2*s) y) ∂volume := by
    rw [← lintegral_indicator
      triangle_measurable,
      Measure.volume_eq_prod,
      lintegral_prod_symm _
        (hf.indicator
          triangle_measurable).aemeasurable,
      ← lintegral_indicator measurableSet_Ioo]
    apply lintegral_congr
    intro y
    by_cases hy : y ∈ Ioo (0:ℝ) 1
    · have hy0 : 0 ≤ y := hy.1.le
      rw [Set.indicator_of_mem hy,
        ← inner_lintegral s y hy0,
        ← lintegral_indicator measurableSet_Ioo]
      apply lintegral_congr
      intro x
      have hm :
          (x,y) ∈ triangle ↔
            x ∈ Ioo 0 y := by
        change
          (0 < x ∧ x < y ∧ y < 1) ↔
          (0 < x ∧ x < y)
        exact ⟨fun h => ⟨h.1,h.2.1⟩,
          fun h => ⟨h.1,h.2,hy.2⟩⟩
      by_cases hx : x ∈ Ioo 0 y
      · rw [Set.indicator_of_mem (hm.mpr hx),
          Set.indicator_of_mem hx]
      · rw [Set.indicator_of_notMem
          (fun h => hx (hm.mp h)),
          Set.indicator_of_notMem hx]
    · rw [Set.indicator_of_notMem hy]
      have hn (x : ℝ) :
          (x,y) ∉ triangle := by
        intro h
        change
          0 < x ∧ x < y ∧ y < 1 at h
        exact hy
          ⟨lt_trans h.1 h.2.1,h.2.2⟩
      simp only [Set.indicator_of_notMem (hn _),
        lintegral_zero]
  have hc : Continuous (Chronos.RadialMoments.inner (2*s)) := by
    let k : ℕ := 2*s
    change Continuous (Chronos.RadialMoments.inner k)
    have heq :
        Chronos.RadialMoments.inner k =
          (fun y : ℝ =>
            y^(k+2) *
              ((y^(k+1)-0^(k+1))/(k+1)) -
            (2*y^(k+1)) *
              ((y^((k+1)+1)-0^((k+1)+1))/
                ((k+1)+1)) +
            y^k *
              ((y^((k+2)+1)-0^((k+2)+1))/
                ((k+2)+1))) :=
      funext (Chronos.RadialMoments.inner_formula k)
    rw [heq]
    fun_prop
  have hi :
      IntervalIntegrable
        (Chronos.RadialMoments.inner (2*s)) volume 0 1 :=
    hc.intervalIntegrable _ _
  have hn :
      0 ≤ᵐ[volume.restrict
        (Ioc (0:ℝ) 1)]
        Chronos.RadialMoments.inner (2*s) := by
    filter_upwards
      [ae_restrict_mem measurableSet_Ioc]
      with y hy
    change 0 ≤ Chronos.RadialMoments.inner (2*s) y
    unfold Chronos.RadialMoments.inner
    exact intervalIntegral.integral_nonneg_of_forall
      hy.1.le
      (fun x =>
        polynomial_nonnegative s x y)
  rw [he,restrict_Ioo_eq_restrict_Ioc,
    ← ofReal_integral_eq_lintegral_ofReal
      hi.1 hn,
    ← intervalIntegral.integral_of_le
      zero_le_one]
  congr 1
  unfold reducedMoment
  ring

theorem radialLaw_weighted
    (s : ℕ) :
    (∫⁻ p in region, radialWeight s p
      ∂((volume : Measure ℝ).prod radialLaw)) =
      ENNReal.ofReal
        (reducedMoment s / 32) := by
  have hd : Measurable density := by
    unfold density
    apply Measurable.ennreal_ofReal
    fun_prop
  have hp :
      (volume : Measure ℝ).prod
        (volume.restrict (Ioc (0:ℝ) 1)) =
      (volume : Measure Plane).restrict
        ((Set.univ : Set ℝ) ×ˢ
          Ioc (0:ℝ) 1) := by
    rw [Measure.volume_eq_prod]
    simpa only [Measure.restrict_univ] using
      (Measure.prod_restrict
        (μ := (volume : Measure ℝ))
        (ν := (volume : Measure ℝ))
        Set.univ (Ioc (0:ℝ) 1))
  rw [radialLaw,prod_withDensity_right hd,
    hp,restrict_withDensity
      region_open.measurableSet,
    Measure.restrict_restrict
      region_open.measurableSet]
  have hweighted :
      (∫⁻ p : Plane, radialWeight s p
        ∂((volume.restrict
          (region ∩ ((Set.univ : Set ℝ) ×ˢ
            Ioc (0:ℝ) 1))).withDensity
              (fun z : Plane => density z.2))) =
        ∫⁻ p : Plane, density p.2 * radialWeight s p
          ∂(volume.restrict
            (region ∩ ((Set.univ : Set ℝ) ×ˢ
              Ioc (0:ℝ) 1))) := by
    exact lintegral_withDensity_eq_lintegral_mul
      _
      (show Measurable (fun z : Plane => density z.2)
        from hd.comp measurable_snd)
      (radialWeight_measurable s)
  rw [hweighted]
  change
    (∫⁻ p in sourceRegion,
      density p.2 * radialWeight s p
        ∂volume) = _
  have he :
      (∫⁻ p in sourceRegion,
        density p.2 * radialWeight s p
          ∂volume) =
        ∫⁻ p in sourceRegion,
          ENNReal.ofReal (3/4) *
            weight s (nullMap p) ∂volume := by
    apply lintegral_congr
    intro p
    unfold density radialWeight weight
    rw [← ENNReal.ofReal_mul
      (show 0 ≤ 3*p.2^2 by positivity),
      null_proper_time_square,
      null_radial_weight,mul_assoc,
      ENNReal.ofReal_mul
        (by norm_num : (0:ℝ) ≤ 3/4)]
  have hm : Measurable
      (fun p : Plane => weight s (nullMap p)) :=
    (weight_measurable s).comp
      nullMap_measurable
  have hmul :
      (∫⁻ p in sourceRegion,
        ENNReal.ofReal (3/4) *
          weight s (nullMap p) ∂volume) =
      ENNReal.ofReal (3/4) *
        (∫⁻ p in sourceRegion,
          weight s (nullMap p) ∂volume) :=
    lintegral_const_mul
      (ENNReal.ofReal (3/4)) hm
  rw [he,hmul,
    null_change_of_variables (weight s)
      (weight_measurable s),
    triangle_lintegral,
    ← ENNReal.ofReal_mul
      (by norm_num : (0:ℝ) ≤ 1/2),
    ← ENNReal.ofReal_mul
      (by norm_num : (0:ℝ) ≤ 3/4)]
  congr 1
  ring

section Physical

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [NormedSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E] [BorelSpace E]

theorem physical_raw_moment
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (s : ℕ) :
    (∫⁻ p in diamond (0:ℝ × E) tip,
      ENNReal.ofReal
        (((1-p.1)^2-‖p.2‖^2)^(2*s))
        ∂((volume : Measure ℝ).prod μ)) =
      μ (Metric.closedBall (0:E) 1) *
        ENNReal.ofReal
          (reducedMoment s / 32) := by
  rw [physical_moment_radial_reduction
    μ hdim s,radialLaw_weighted]

theorem physical_diamond_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((volume : Measure ℝ).prod μ)
      (diamond (0:ℝ × E) tip) =
      μ (Metric.closedBall (0:E) 1) *
        ENNReal.ofReal (1/32) := by
  simpa [Chronos.RadialMoments.moment_zero]
    using physical_raw_moment μ hdim 0

theorem normalized_physical_moment
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (s : ℕ) :
    (∫⁻ p,
      ENNReal.ofReal
        (((1-p.1)^2-‖p.2‖^2)^(2*s))
      ∂Chronos.GeometricTransport.normalized
        (((volume : Measure ℝ).prod μ).restrict
          (diamond (0:ℝ × E) tip))) =
        ENNReal.ofReal (reducedMoment s) := by
  let C := μ (Metric.closedBall (0:E) 1)
  have hC0 : C ≠ 0 :=
    (Metric.measure_closedBall_pos μ
      (0:E) zero_lt_one).ne'
  have hCT : C ≠ ∞ :=
    (isCompact_closedBall
      (0:E) 1).measure_lt_top.ne
  let A : ℝ≥0∞ :=
    C * ENNReal.ofReal (1/32)
  have hA0 : A ≠ 0 := by
    dsimp [A]
    exact mul_ne_zero hC0
      (by norm_num)
  have hAT : A ≠ ∞ := by
    dsimp [A]
    exact ENNReal.mul_ne_top hCT
      ENNReal.ofReal_ne_top
  unfold Chronos.GeometricTransport.normalized
  rw [lintegral_smul_measure,
    smul_eq_mul,
    Measure.restrict_apply_univ,
    physical_diamond_mass μ hdim,
    physical_raw_moment μ hdim s]
  have hsplit :
      ENNReal.ofReal
        (reducedMoment s / 32) =
      ENNReal.ofReal (1/32) *
        ENNReal.ofReal (reducedMoment s) := by
    rw [← ENNReal.ofReal_mul
      (by norm_num : (0:ℝ) ≤ 1/32)]
    congr 1
    ring
  rw [hsplit]
  calc
    _ = A⁻¹ * (A *
        ENNReal.ofReal (reducedMoment s)) := by
      dsimp only [A,C]
      ac_rfl
    _ = _ :=
      ENNReal.inv_mul_cancel_left hA0 hAT

end Physical

#print axioms weight_measurable
#print axioms polynomial_nonnegative
#print axioms inner_lintegral
#print axioms triangle_lintegral
#print axioms radialLaw_weighted
#print axioms physical_raw_moment
#print axioms physical_diamond_mass
#print axioms normalized_physical_moment

end Chronos.NormalizedMoments

open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.FutureMoments

open Chronos.MinkowskiDiamond
open Chronos.MinkowskiProbability
open Chronos.NormalizedMoments

variable {E : Type*}
variable [NormedAddCommGroup E]

theorem precedes_transitive
    {a b c : ℝ × E}
    (hab : precedes a b)
    (hbc : precedes b c) :
    precedes a c := by
  change ‖b.2-a.2‖ < b.1-a.1 at hab
  change ‖c.2-b.2‖ < c.1-b.1 at hbc
  change ‖c.2-a.2‖ < c.1-a.1
  have he :
      c.2-a.2 =
        (c.2-b.2)+(b.2-a.2) := by
    abel
  rw [he]
  have hn :=
    norm_add_le
      (c.2-b.2) (b.2-a.2)
  linarith

def futureSet (p : ℝ × E) :
    Set (ℝ × E) :=
  {q | precedes p q}

theorem futureSet_open (p : ℝ × E) :
    IsOpen (futureSet p) := by
  have h1 : Continuous
      (fun q : ℝ × E =>
        ‖q.2-p.2‖) := by
    fun_prop
  have h2 : Continuous
      (fun q : ℝ × E =>
        q.1-p.1) := by
    fun_prop
  exact isOpen_lt h1 h2

theorem future_inter_diamond
    {p : ℝ × E}
    (hp : p ∈ diamond (0:ℝ × E) tip) :
    futureSet p ∩
      diamond (0:ℝ × E) tip =
      diamond p tip := by
  change precedes 0 p ∧
    precedes p tip at hp
  ext q
  change
    (precedes p q ∧
      (precedes 0 q ∧ precedes q tip)) ↔
      (precedes p q ∧ precedes q tip)
  constructor
  · rintro ⟨h1,_,h2⟩
    exact ⟨h1,h2⟩
  · rintro ⟨h1,h2⟩
    exact ⟨h1,
      precedes_transitive hp.1 h1,h2⟩

section Haar

variable [InnerProductSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E]
variable [BorelSpace E]

noncomputable def futureMass
    (μ : Measure E) (p : ℝ × E) :
    ℝ≥0∞ :=
  uniform
    ((volume : Measure ℝ).prod μ)
    (0:ℝ × E) tip
    (futureSet p)

theorem future_volume_ratio
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (p : ℝ × E)
    (hp : p ∈ diamond (0:ℝ × E) tip) :
    ((volume : Measure ℝ).prod μ)
      (diamond p tip) =
    ENNReal.ofReal
      (((1-p.1)^2-‖p.2‖^2)^2) *
      ((volume : Measure ℝ).prod μ)
        (diamond (0:ℝ × E) tip) := by
  let ν := (volume : Measure ℝ).prod μ
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  change precedes 0 p ∧
    precedes p tip at hp
  have ht : ‖p.2‖ < 1-p.1 := by
    simpa [precedes,tip] using hp.2
  have htime : 0 < 1-p.1 :=
    lt_of_le_of_lt (norm_nonneg _) ht
  have hsq :
      0 ≤ (1-p.1)^2-‖p.2‖^2 := by
    nlinarith [mul_nonneg
      (sub_nonneg.mpr ht.le)
      (add_nonneg htime.le
        (norm_nonneg p.2))]
  have hdim4 :
      Module.finrank ℝ (ℝ × E) = 4 := by
    simp [Module.finrank_prod,hdim]
  have hpow :
      Real.sqrt
        ((1-p.1)^2-‖p.2‖^2)^4 =
        ((1-p.1)^2-‖p.2‖^2)^2 := by
    calc
      _ = (Real.sqrt
          ((1-p.1)^2-‖p.2‖^2)^2)^2 := by
        ring
      _ = _ := by rw [Real.sq_sqrt hsq]
  have hv :=
    Chronos.MinkowskiVolume.diamond_volume_scaling
      ν p tip hp.2
  simpa only [tip,zero_sub,norm_neg,
    hdim4,hpow] using hv

theorem future_mass_polynomial
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (p : ℝ × E)
    (hp : p ∈ diamond (0:ℝ × E) tip) :
    futureMass μ p =
      ENNReal.ofReal
        (((1-p.1)^2-‖p.2‖^2)^2) := by
  let ν := (volume : Measure ℝ).prod μ
  let D := diamond (0:ℝ × E) tip
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  have hab : precedes
      (0:ℝ × E) tip := by
    norm_num [precedes,tip]
  have hD :
      0 < ν D ∧ ν D < ∞ :=
    diamond_volume_bounds ν 0 tip hab
  have hv :=
    future_volume_ratio μ hdim p hp
  unfold futureMass uniform
    Chronos.GeometricTransport.normalized
  rw [Measure.smul_apply,smul_eq_mul,
    Measure.restrict_apply_univ,
    Measure.restrict_apply
      (futureSet_open p).measurableSet,
    future_inter_diamond hp,hv]
  calc
    _ = (ν D)⁻¹ *
        (ν D * ENNReal.ofReal
          (((1-p.1)^2-‖p.2‖^2)^2)) := by
      dsimp only [ν,D]
      ac_rfl
    _ = _ :=
      ENNReal.inv_mul_cancel_left
        hD.1.ne' hD.2.ne

theorem future_moment
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (s : ℕ) :
    (∫⁻ p, (futureMass μ p)^s
      ∂uniform
        ((volume : Measure ℝ).prod μ)
        (0:ℝ × E) tip) =
    ENNReal.ofReal
      (Chronos.RadialMoments.reducedMoment s) := by
  let ν := (volume : Measure ℝ).prod μ
  let D := diamond (0:ℝ × E) tip
  let ρ := uniform ν (0:ℝ × E) tip
  have hsupport :
      ∀ᵐ p ∂ρ, p ∈ D := by
    have hm : MeasurableSet D :=
      (diamond_open (0:ℝ × E)
        tip).measurableSet
    change ∀ᵐ p ∂
      ((ν.restrict D Set.univ)⁻¹ •
        ν.restrict D), p ∈ D
    exact Measure.ae_smul_measure
      (ae_restrict_mem hm) _
  change
    (∫⁻ p,(futureMass μ p)^s ∂ρ) = _
  calc
    _ =
      ∫⁻ p,
        ENNReal.ofReal
          (((1-p.1)^2-‖p.2‖^2)^(2*s))
        ∂ρ := by
      apply lintegral_congr_ae
      filter_upwards [hsupport] with p hp
      rw [future_mass_polynomial μ hdim p hp,
        pow_mul,
        ENNReal.ofReal_pow
          (sq_nonneg _) s]
    _ = _ :=
      normalized_physical_moment μ hdim s

theorem future_first_moment
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (∫⁻ p, futureMass μ p
      ∂uniform
        ((volume : Measure ℝ).prod μ)
        (0:ℝ × E) tip) =
      ENNReal.ofReal (1/20) := by
  simpa only [pow_one,
    Chronos.RadialMoments.moment_one]
      using future_moment μ hdim 1

theorem future_second_moment
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (∫⁻ p, (futureMass μ p)^2
      ∂uniform
        ((volume : Measure ℝ).prod μ)
        (0:ℝ × E) tip) =
      ENNReal.ofReal (1/105) := by
  simpa only
    [Chronos.RadialMoments.moment_two]
      using future_moment μ hdim 2

end Haar

#print axioms precedes_transitive
#print axioms futureSet_open
#print axioms future_inter_diamond
#print axioms future_volume_ratio
#print axioms future_mass_polynomial
#print axioms future_moment
#print axioms future_first_moment
#print axioms future_second_moment

end Chronos.FutureMoments

open MeasureTheory Set
open scoped ENNReal Interval

namespace Chronos.ThreeEvent

open Chronos.MinkowskiDiamond
open Chronos.MinkowskiProbability
open Chronos.FutureMoments

variable {E : Type*}
variable [NormedAddCommGroup E]

abbrev Spacetime (E : Type*) := ℝ × E

def causalPair : Set
    (Spacetime E × Spacetime E) :=
  {z | precedes z.1 z.2}

theorem causalPair_open :
    IsOpen (causalPair (E := E)) := by
  have h1 : Continuous
      (fun z : Spacetime E × Spacetime E =>
        ‖z.2.2-z.1.2‖) := by
    fun_prop
  have h2 : Continuous
      (fun z : Spacetime E × Spacetime E =>
        z.2.1-z.1.1) := by
    fun_prop
  exact isOpen_lt h1 h2

def forkEvent : Set
    (Spacetime E ×
      (Spacetime E × Spacetime E)) :=
  {z | precedes z.1 z.2.1 ∧
       precedes z.1 z.2.2}

def earliestComparable : Set
    (Spacetime E ×
      (Spacetime E × Spacetime E)) :=
  forkEvent ∩
    Prod.snd ⁻¹' comparable

theorem forkEvent_open :
    IsOpen (forkEvent (E := E)) := by
  have h1 : Continuous
      (fun z : Spacetime E ×
        (Spacetime E × Spacetime E) =>
        (z.1,z.2.1)) := by fun_prop
  have h2 : Continuous
      (fun z : Spacetime E ×
        (Spacetime E × Spacetime E) =>
        (z.1,z.2.2)) := by fun_prop
  exact
    (causalPair_open.preimage h1).inter
      (causalPair_open.preimage h2)

section Probability

variable [InnerProductSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E]
variable [BorelSpace E]

noncomputable def law
    (μ : Measure E) :
    Measure (Spacetime E) :=
  uniform
    ((volume : Measure ℝ).prod μ)
    (0:Spacetime E) tip

omit [FiniteDimensional ℝ E] in
theorem law_probability
    (μ : Measure E)
    [μ.IsAddHaarMeasure] :
    IsProbabilityMeasure (law μ) := by
  let ν := (volume : Measure ℝ).prod μ
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  have hab : precedes
      (0:Spacetime E) tip := by
    norm_num [precedes,tip]
  exact uniform_probability ν 0 tip hab

omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] in
theorem law_support
    (μ : Measure E) :
    ∀ᵐ p ∂law μ,
      p ∈ diamond (0:Spacetime E) tip := by
  let ν := (volume : Measure ℝ).prod μ
  let D := diamond (0:Spacetime E) tip
  have hm : MeasurableSet D :=
    (diamond_open (0:Spacetime E)
      tip).measurableSet
  change ∀ᵐ p ∂
    ((ν.restrict D Set.univ)⁻¹ •
      ν.restrict D), p ∈ D
  exact Measure.ae_smul_measure
    (ae_restrict_mem hm) _

omit [FiniteDimensional ℝ E] in
theorem futureMass_measurable
    (μ : Measure E)
    [μ.IsAddHaarMeasure] :
    Measurable (futureMass μ) := by
  letI : IsProbabilityMeasure (law μ) :=
    law_probability μ
  have h :=
    measurable_measure_prodMk_left
      (ν := law μ)
      (causalPair_open (E := E)).measurableSet
  exact h

theorem directed_pair_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((law μ).prod (law μ)) causalPair =
      ENNReal.ofReal (1/20) := by
  letI : IsProbabilityMeasure (law μ) :=
    law_probability μ
  rw [Measure.prod_apply
    causalPair_open.measurableSet]
  change
    (∫⁻ p, futureMass μ p ∂law μ) = _
  exact future_first_moment μ hdim

theorem comparable_pair_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((law μ).prod (law μ)) comparable =
      ENNReal.ofReal (1/10) := by
  let ρ := law μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  let S : Set
      (Spacetime E × Spacetime E) :=
    causalPair
  let T := Prod.swap ⁻¹' S
  have hs : MeasurableSet S :=
    causalPair_open.measurableSet
  have ht : MeasurableSet T :=
    measurable_swap hs
  have hu :
      comparable = S ∪ T := by
    ext z
    rfl
  have hd : Disjoint S T := by
    rw [Set.disjoint_left]
    intro z hz hw
    change precedes z.1 z.2 at hz
    change precedes z.2 z.1 at hw
    change
      ‖z.2.2-z.1.2‖ <
        z.2.1-z.1.1 at hz
    change
      ‖z.1.2-z.2.2‖ <
        z.1.1-z.2.1 at hw
    linarith [norm_nonneg (z.2.2-z.1.2),
      norm_nonneg (z.1.2-z.2.2)]
  have hswap :
      (ρ.prod ρ).map Prod.swap =
        ρ.prod ρ :=
    Measure.prod_swap
  have hT :
      (ρ.prod ρ) T =
        (ρ.prod ρ) S := by
    change
      (ρ.prod ρ) (Prod.swap ⁻¹' S) = _
    rw [← Measure.map_apply
      measurable_swap hs,hswap]
  have hS :
      (ρ.prod ρ) S =
        ENNReal.ofReal (1/20) :=
    directed_pair_mass μ hdim
  change (ρ.prod ρ) comparable = _
  rw [hu,measure_union hd ht,hT,hS,
    ← ENNReal.ofReal_add
      (by norm_num : (0:ℝ) ≤ 1/20)
      (by norm_num : (0:ℝ) ≤ 1/20)]
  congr 1
  norm_num

theorem fork_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((law μ).prod
      ((law μ).prod (law μ))) forkEvent =
        ENNReal.ofReal (1/105) := by
  let ρ := law μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  change (ρ.prod (ρ.prod ρ)) forkEvent = _
  rw [Measure.prod_apply
    forkEvent_open.measurableSet]
  calc
    _ =
      ∫⁻ p, (futureMass μ p)^2 ∂ρ := by
      apply lintegral_congr
      intro p
      have he :
          Prod.mk p ⁻¹' forkEvent =
            futureSet p ×ˢ futureSet p := by
        ext z
        rfl
      rw [he,Measure.prod_prod,pow_two]
      rfl
    _ = _ :=
      future_second_moment μ hdim

omit [FiniteDimensional ℝ E] in
theorem future_restriction
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (p : Spacetime E)
    (hp : p ∈ diamond
      (0:Spacetime E) tip) :
    (law μ).restrict (futureSet p) =
      futureMass μ p •
        uniform
          ((volume : Measure ℝ).prod μ)
          p tip := by
  let ν := (volume : Measure ℝ).prod μ
  let D := diamond (0:Spacetime E) tip
  let J := diamond p tip
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  have hab : precedes p tip := hp.2
  have hJ :
      0 < ν J ∧ ν J < ∞ :=
    diamond_volume_bounds ν p tip hab
  have hm :
      futureMass μ p =
        (ν D)⁻¹ * ν J := by
    unfold futureMass uniform
      Chronos.GeometricTransport.normalized
    rw [Measure.smul_apply,smul_eq_mul,
      Measure.restrict_apply_univ,
      Measure.restrict_apply
        (futureSet_open p).measurableSet,
      future_inter_diamond hp]
  have hc :
      ((ν D)⁻¹ * ν J) * (ν J)⁻¹ =
        (ν D)⁻¹ := by
    rw [mul_assoc,
      ENNReal.mul_inv_cancel
        hJ.1.ne' hJ.2.ne,mul_one]
  rw [hm]
  unfold law uniform
    Chronos.GeometricTransport.normalized
  rw [Measure.restrict_smul,
    Measure.restrict_restrict
      (futureSet_open p).measurableSet,
    future_inter_diamond hp,
    Measure.restrict_apply_univ,
    Measure.restrict_apply_univ,
    smul_smul]
  change
    (ν D)⁻¹ • ν.restrict J =
      (((ν D)⁻¹ * ν J) * (ν J)⁻¹) •
        ν.restrict J
  rw [hc]

theorem earliest_section_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (p : Spacetime E)
    (hp : p ∈ diamond
      (0:Spacetime E) tip) :
    ((law μ).prod (law μ))
      (Prod.mk p ⁻¹' earliestComparable) =
      ENNReal.ofReal (1/10) *
        (futureMass μ p)^2 := by
  let ν := (volume : Measure ℝ).prod μ
  let ρ := law μ
  let η := uniform ν p tip
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  letI : IsProbabilityMeasure η :=
    uniform_probability ν p tip hp.2
  have he :
      Prod.mk p ⁻¹' earliestComparable =
        comparable ∩
          (futureSet p ×ˢ futureSet p) := by
    ext z
    change
      ((precedes p z.1 ∧
        precedes p z.2) ∧
          z ∈ comparable) ↔
      (z ∈ comparable ∧
        (precedes p z.1 ∧
          precedes p z.2))
    tauto
  have hpair :
      (η.prod η) comparable =
        ENNReal.ofReal (1/10) := by
    change pairProbability ν p tip = _
    rw [pair_probability_invariant
      ν p tip hp.2]
    exact comparable_pair_mass μ hdim
  have hr :
      ρ.restrict (futureSet p) =
        futureMass μ p • η :=
    future_restriction μ p hp
  change
    (ρ.prod ρ)
      (Prod.mk p ⁻¹' earliestComparable) = _
  rw [he]
  calc
    _ =
      ((ρ.restrict (futureSet p)).prod
        (ρ.restrict (futureSet p)))
          comparable := by
      rw [Measure.prod_restrict,
        Measure.restrict_apply
          comparable_open.measurableSet]
    _ = _ := by
      rw [hr,Measure.prod_smul_left,
        Measure.prod_smul_right]
      simp only [Measure.smul_apply,
        smul_eq_mul,hpair,pow_two]
      ac_rfl

theorem earliest_comparable_mass
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((law μ).prod
      ((law μ).prod (law μ)))
        earliestComparable =
      ENNReal.ofReal (1/1050) := by
  let ρ := law μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  have he :
      MeasurableSet
        (earliestComparable (E := E)) :=
    forkEvent_open.measurableSet.inter
      (measurable_snd
        comparable_open.measurableSet)
  have hs :
      ∀ᵐ p ∂ρ,
        p ∈ diamond (0:Spacetime E) tip :=
    law_support μ
  change
    (ρ.prod (ρ.prod ρ))
      earliestComparable = _
  rw [Measure.prod_apply he]
  have hpow :
      Measurable
        (fun p : Spacetime E =>
          (futureMass μ p)^2) :=
    (futureMass_measurable μ).pow_const 2
  calc
    _ =
      ∫⁻ p,
        ENNReal.ofReal (1/10) *
          (futureMass μ p)^2 ∂ρ := by
      apply lintegral_congr_ae
      filter_upwards [hs] with p hp
      exact earliest_section_mass μ hdim p hp
    _ = ENNReal.ofReal (1/10) *
          (∫⁻ p,
            (futureMass μ p)^2 ∂ρ) :=
      lintegral_const_mul _ hpow
    _ = _ := by
      rw [show
        (∫⁻ p, (futureMass μ p)^2 ∂ρ) =
          ENNReal.ofReal (1/105) from
            future_second_moment μ hdim,
        ← ENNReal.ofReal_mul
          (by norm_num : (0:ℝ) ≤ 1/10)]
      congr 1
      norm_num

end Probability

#print axioms causalPair_open
#print axioms forkEvent_open
#print axioms law_probability
#print axioms law_support
#print axioms futureMass_measurable
#print axioms directed_pair_mass
#print axioms comparable_pair_mass
#print axioms fork_mass
#print axioms future_restriction
#print axioms earliest_section_mass
#print axioms earliest_comparable_mass

end Chronos.ThreeEvent

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.ThreeDistribution

open Chronos.MinkowskiDiamond
open Chronos.MinkowskiProbability
open Chronos.FutureMoments
open Chronos.ThreeEvent

variable {E : Type*}
variable [NormedAddCommGroup E]

abbrev Triple (E : Type*) :=
  Spacetime E × (Spacetime E × Spacetime E)

def rotate (z : Triple E) : Triple E :=
  (z.2.1,z.2.2,z.1)

def reversePoint (p : Spacetime E) :
    Spacetime E :=
  -p + tip

def reverseTriple (z : Triple E) :
    Triple E :=
  (reversePoint z.1,
    reversePoint z.2.1,
    reversePoint z.2.2)

theorem reverse_precedes
    (p q : Spacetime E) :
    precedes (reversePoint p)
      (reversePoint q) ↔
    precedes q p := by
  change
    ‖(-q.2+0)-(-p.2+0)‖ <
      (-q.1+1)-(-p.1+1) ↔
    ‖p.2-q.2‖ < p.1-q.1
  simp only [add_zero]
  have hx : -q.2 - -p.2 = p.2-q.2 := by
    abel
  have ht :
      (-q.1+1)-(-p.1+1) =
        p.1-q.1 := by ring
  rw [hx,ht]

theorem precedes_asymmetric
    {p q : Spacetime E}
    (h : precedes p q) :
    ¬ precedes q p := by
  intro k
  change ‖q.2-p.2‖ < q.1-p.1 at h
  change ‖p.2-q.2‖ < p.1-q.1 at k
  linarith [norm_nonneg (q.2-p.2),
    norm_nonneg (p.2-q.2)]

section Probability

variable [InnerProductSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E]
variable [BorelSpace E]

noncomputable def tripleLaw
    (μ : Measure E) : Measure (Triple E) :=
  (law μ).prod ((law μ).prod (law μ))

theorem reverse_law
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (law μ).map reversePoint = law μ := by
  let ν := (volume : Measure ℝ).prod μ
  let D := diamond (0:Spacetime E) tip
  letI : ν.IsAddHaarMeasure := by
    change ((volume : Measure ℝ).prod
      μ).IsAddHaarMeasure
    infer_instance
  let L : Spacetime E →ₗ[ℝ] Spacetime E :=
    (-1:ℝ) • LinearMap.id
  have hdim4 :
      Module.finrank ℝ (Spacetime E) = 4 := by
    simp [Spacetime,Module.finrank_prod,hdim]
  have hd : LinearMap.det L = 1 := by
    norm_num [L,LinearMap.det_smul,hdim4]
  have hL :
      (L : Spacetime E → Spacetime E) =
        (fun p => -p) := by
    funext p
    simp [L]
  have hneg :
      ν.map (fun p : Spacetime E => -p) =
        ν := by
    have h :=
      Measure.map_linearMap_addHaar_eq_smul_addHaar
        ν (f := L) (by rw [hd]; norm_num)
    rw [hL,hd] at h
    simpa using h
  have ht :
      ν.map (fun p : Spacetime E =>
        p+tip) = ν :=
    map_add_right_eq_self ν tip
  have hn :
      Measurable
        (fun p : Spacetime E => -p) := by
    fun_prop
  have ha :
      Measurable
        (fun p : Spacetime E => p+tip) := by
    fun_prop
  have hf : Measurable
      (reversePoint : Spacetime E →
        Spacetime E) :=
    ha.comp hn
  have hmap : ν.map reversePoint = ν := by
    change ν.map
      ((fun p : Spacetime E => p+tip) ∘
        (fun p : Spacetime E => -p)) = ν
    rw [← Measure.map_map ha hn,hneg,ht]
  have h0 :
      reversePoint (0:Spacetime E) = tip := by
    simp [reversePoint]
  have htip :
      reversePoint (tip : Spacetime E) = 0 := by
    simp [reversePoint]
  have hD : reversePoint ⁻¹' D = D := by
    ext p
    change
      (precedes 0 (reversePoint p) ∧
        precedes (reversePoint p) tip) ↔
      (precedes 0 p ∧ precedes p tip)
    have h1 :
        precedes 0 (reversePoint p) ↔
          precedes p tip := by
      simpa only [htip] using
        reverse_precedes tip p
    have h2 :
        precedes (reversePoint p) tip ↔
          precedes 0 p := by
      simpa only [h0] using
        reverse_precedes p (0:Spacetime E)
    rw [h1,h2,and_comm]
  have hm : MeasurableSet D :=
    (diamond_open (0:Spacetime E)
      tip).measurableSet
  have hr :
      (ν.restrict D).map reversePoint =
        ν.restrict D := by
    have h := Measure.restrict_map
      (μ := ν) hf hm
    rw [hmap,hD] at h
    exact h.symm
  unfold law uniform
    Chronos.GeometricTransport.normalized
  change
    (((ν.restrict D) Set.univ)⁻¹ •
      ν.restrict D).map reversePoint =
    ((ν.restrict D) Set.univ)⁻¹ •
      ν.restrict D
  rw [Measure.map_smul,hr]

omit [FiniteDimensional ℝ E] in
theorem rotate_law
    (μ : Measure E)
    [μ.IsAddHaarMeasure] :
    (tripleLaw μ).map rotate =
      tripleLaw μ := by
  let ρ := law μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  let a :
      (Spacetime E × Spacetime E) ×
        Spacetime E ≃ᵐ Triple E :=
    MeasurableEquiv.prodAssoc
  have h :
      ((ρ.prod ρ).prod ρ).map a =
        ρ.prod (ρ.prod ρ) :=
    (measurePreserving_prodAssoc ρ ρ ρ).map_eq
  change
    (ρ.prod (ρ.prod ρ)).map
      (a ∘ Prod.swap) =
        ρ.prod (ρ.prod ρ)
  rw [← Measure.map_map
    a.measurable measurable_swap,
    Measure.prod_swap]
  exact h

theorem reverse_triple_law
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    (tripleLaw μ).map reverseTriple =
      tripleLaw μ := by
  let ρ := law μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  have hf : Measurable
      (reversePoint : Spacetime E →
        Spacetime E) := by
    unfold reversePoint
    fun_prop
  have hr : ρ.map reversePoint = ρ :=
    reverse_law μ hdim
  change
    (ρ.prod (ρ.prod ρ)).map
      (Prod.map reversePoint
        (Prod.map reversePoint reversePoint)) =
      ρ.prod (ρ.prod ρ)
  rw [← Measure.map_prod_map
    ρ (ρ.prod ρ) hf (hf.prodMap hf),
    ← Measure.map_prod_map ρ ρ hf hf]
  simp only [hr]

end Probability

