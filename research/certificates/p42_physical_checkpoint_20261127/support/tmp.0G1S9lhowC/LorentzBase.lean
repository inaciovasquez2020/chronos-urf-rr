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
