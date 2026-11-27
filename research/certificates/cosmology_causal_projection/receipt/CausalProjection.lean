import Mathlib.Tactic

namespace Chronos.CosmologyBridge

noncomputable def stripArea (a b d : ℝ) : ℝ :=
  if d ≤ |a-b| then
    4 * min a b * d
  else if d ≤ a+b then
    4*a*b - (a+b-d)^2
  else
    4*a*b

noncomputable def stripProbability (a b d : ℝ) : ℝ :=
  stripArea a b d / (4*a*b)

theorem stripArea_closed (a b d : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hd : 0 ≤ d) :
    stripArea a b d =
      4*a*b - (max (a+b-d) 0)^2 +
        (max (|a-b|-d) 0)^2 := by
  have habs : |a-b| ≤ a+b :=
    abs_le.mpr ⟨by linarith,by linarith⟩
  by_cases hsmall : d ≤ |a-b|
  · have hsum : d ≤ a+b := hsmall.trans habs
    rw [stripArea,if_pos hsmall,
      max_eq_left (sub_nonneg.mpr hsum),
      max_eq_left (sub_nonneg.mpr hsmall)]
    rcases le_total a b with h | h
    · rw [min_eq_left h,
        abs_of_nonpos (sub_nonpos.mpr h)]
      ring
    · rw [min_eq_right h,
        abs_of_nonneg (sub_nonneg.mpr h)]
      ring
  · have hh : |a-b| ≤ d := by linarith
    by_cases hsum : d ≤ a+b
    · rw [stripArea,if_neg hsmall,if_pos hsum,
        max_eq_left (sub_nonneg.mpr hsum),
        max_eq_right (sub_nonpos.mpr hh)]
      ring
    · have hs : a+b ≤ d := by linarith
      rw [stripArea,if_neg hsmall,if_neg hsum,
        max_eq_right (sub_nonpos.mpr hs),
        max_eq_right (sub_nonpos.mpr hh)]
      ring

theorem stripArea_bounds (a b d : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hd : 0 ≤ d) :
    0 ≤ stripArea a b d ∧
      stripArea a b d ≤ 4*a*b := by
  by_cases hsmall : d ≤ |a-b|
  · rw [stripArea,if_pos hsmall]
    rcases le_total a b with h | h
    · rw [min_eq_left h]
      rw [abs_of_nonpos (sub_nonpos.mpr h)] at hsmall
      have hdb : d ≤ b := by linarith
      have hm := mul_le_mul_of_nonneg_left hdb ha.le
      constructor <;>
        nlinarith [mul_nonneg ha.le hd]
    · rw [min_eq_right h]
      rw [abs_of_nonneg (sub_nonneg.mpr h)] at hsmall
      have hda : d ≤ a := by linarith
      have hm := mul_le_mul_of_nonneg_left hda hb.le
      constructor <;>
        nlinarith [mul_nonneg hb.le hd]
  · by_cases hsum : d ≤ a+b
    · have h1 : a-b ≤ |a-b| := le_abs_self _
      have h2 : b-a ≤ |a-b| := by
        calc
          b-a = -(a-b) := by ring
          _ ≤ |a-b| := neg_le_abs _
      have hda : a+b-d ≤ 2*a := by linarith
      have hdb : a+b-d ≤ 2*b := by linarith
      have hprod :=
        mul_le_mul hda hdb
          (sub_nonneg.mpr hsum)
          (show 0 ≤ 2*a by linarith)
      rw [stripArea,if_neg hsmall,if_pos hsum]
      constructor <;>
        nlinarith [sq_nonneg (a+b-d)]
    · rw [stripArea,if_neg hsmall,if_neg hsum]
      exact ⟨by positivity,le_rfl⟩

theorem probability_closed (a b d : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hd : 0 ≤ d) :
    stripProbability a b d =
      1 - ((max (a+b-d) 0)^2 -
        (max (|a-b|-d) 0)^2)/(4*a*b) := by
  rw [stripProbability,stripArea_closed a b d ha hb hd]
  field_simp [ne_of_gt ha,ne_of_gt hb] <;> ring

theorem probability_bounds (a b d : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hd : 0 ≤ d) :
    0 ≤ stripProbability a b d ∧
      stripProbability a b d ≤ 1 := by
  obtain ⟨hl,hu⟩ := stripArea_bounds a b d ha hb hd
  have hp : 0 < 4*a*b := by positivity
  unfold stripProbability
  refine ⟨div_nonneg hl hp.le,?_⟩
  apply (div_le_iff₀ hp).2
  simpa using hu

structure Event where
  s : ℝ
  x1 : ℝ
  x2 : ℝ
  x3 : ℝ
  z : ℝ

abbrev Visible := ℝ × ℝ × ℝ × ℝ

def project (P : Event) : Visible :=
  (P.s,P.x1,P.x2,P.x3)

def diamond (P : Event) : Prop :=
  |P.s| ≤ 1 ∧
    P.x1^2 + P.x2^2 + P.x3^2 + P.z^2
      ≤ (1-|P.s|)^2

def comparable (P Q : Event) : Prop :=
  (P.x1-Q.x1)^2 +
  (P.x2-Q.x2)^2 +
  (P.x3-Q.x3)^2 +
  (P.z-Q.z)^2 ≤ (P.s-Q.s)^2

theorem projection_collision :
    ∃ P Q P' Q' : Event,
      diamond P ∧ diamond Q ∧
      diamond P' ∧ diamond Q' ∧
      project P = project P' ∧
      project Q = project Q' ∧
      comparable P Q ∧
      ¬ comparable P' Q' := by
  refine ⟨⟨-1/4,0,0,0,0⟩,
          ⟨1/4,0,0,0,0⟩,
          ⟨-1/4,0,0,0,-1/2⟩,
          ⟨1/4,0,0,0,1/2⟩,?_⟩
  norm_num [diamond,project,comparable]

theorem no_perfect_visible_decoder :
    ¬ ∃ f : Visible → Visible → Bool,
      ∀ P Q, diamond P → diamond Q →
        (f (project P) (project Q) = true ↔
          comparable P Q) := by
  rintro ⟨f,hf⟩
  obtain ⟨P,Q,P',Q',hP,hQ,hP',hQ',hp,hq,hc,hnc⟩ :=
    projection_collision
  have ht := (hf P Q hP hQ).2 hc
  have ht' :
      f (project P') (project Q') = true := by
    rw [← hp,← hq]
    exact ht
  exact hnc ((hf P' Q' hP' hQ').1 ht')

noncomputable def risk (p : ℝ) (decision : Bool) : ℝ :=
  if decision then 1-p else p

noncomputable def decode (p : ℝ) : Bool :=
  if p ≤ 1-p then false else true

theorem risk_lower (p : ℝ) (b : Bool) :
    min p (1-p) ≤ risk p b := by
  cases b
  · simpa [risk] using min_le_left p (1-p)
  · simpa [risk] using min_le_right p (1-p)

theorem risk_decode (p : ℝ) :
    risk p (decode p) = min p (1-p) := by
  by_cases h : p ≤ 1-p
  · simp [decode,risk,h,min_eq_left h]
  · have h' : 1-p ≤ p := by linarith
    simp [decode,risk,h,min_eq_right h']

theorem optimal_decoder (p : ℝ) :
    IsLeast {e : ℝ | ∃ b : Bool, risk p b = e}
      (min p (1-p)) := by
  refine ⟨⟨decode p,risk_decode p⟩,?_⟩
  rintro e ⟨b,rfl⟩
  exact risk_lower p b

theorem positive_information_loss (p : ℝ)
    (hp : 0 < p) (h1 : p < 1) :
    0 < min p (1-p) := by
  exact lt_min hp (by linarith)

theorem strip_optimal_decoder (a b d : ℝ) :
    IsLeast
      {e : ℝ | ∃ decision : Bool,
        risk (stripProbability a b d) decision = e}
      (min (stripProbability a b d)
        (1-stripProbability a b d)) :=
  optimal_decoder _

#print axioms stripArea_closed
#print axioms stripArea_bounds
#print axioms probability_closed
#print axioms probability_bounds
#print axioms projection_collision
#print axioms no_perfect_visible_decoder
#print axioms risk_lower
#print axioms risk_decode
#print axioms optimal_decoder
#print axioms positive_information_loss
#print axioms strip_optimal_decoder

end Chronos.CosmologyBridge
