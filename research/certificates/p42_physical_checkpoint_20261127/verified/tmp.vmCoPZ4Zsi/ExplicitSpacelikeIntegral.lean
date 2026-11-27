import SpacelikeMomentReduction
import Mathlib.MeasureTheory.Function.JacobianOneDim

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

open Chronos.NullCoordinates

noncomputable section

theorem rapidityRadial_coordinates
    (p : Plane) :
    rapidityRadial p =
      (1-Real.exp (-p.1)*Real.cosh p.2,
       Real.exp (-p.1)*Real.sinh p.2) := by

  change
    (1-(Real.exp (-p.1-p.2)+
        Real.exp (-p.1+p.2))/2,
     (Real.exp (-p.1+p.2)-
        Real.exp (-p.1-p.2))/2) = _

  rw [Real.cosh_eq,Real.sinh_eq,
    sub_eq_add_neg (-p.1) p.2,
    Real.exp_add (-p.1) (-p.2),
    Real.exp_add (-p.1) p.2]

  apply Prod.ext <;> dsimp only <;> ring

theorem rapidityRadial_proper
    (p : Plane) :
    radialProperSq (rapidityRadial p) =
      (Real.exp (-p.1))^2 := by

  rw [rapidityRadial_coordinates]

  unfold radialProperSq
  dsimp only

  linear_combination
    (Real.exp (-p.1))^2 *
      Real.cosh_sq_sub_sinh_sq p.2

private theorem exp_cosh_difference
    (l m : ℝ) :
    2*(Real.exp (-l)*Real.exp (-m)) *
      Real.cosh (l-m) =
        (Real.exp (-l))^2 +
        (Real.exp (-m))^2 := by

  have h1 :
      Real.exp (-l)*Real.exp (-m)*
        Real.exp (l-m) =
        (Real.exp (-m))^2 := by

    calc
      _ = Real.exp
          ((-l + -m)+(l-m)) := by
        simp only [Real.exp_add]

      _ = _ := by
        rw [pow_two,← Real.exp_add]
        congr 1
        ring

  have h2 :
      Real.exp (-l)*Real.exp (-m)*
        Real.exp (-(l-m)) =
        (Real.exp (-l))^2 := by

    calc
      _ = Real.exp
          ((-l + -m)+(-(l-m))) := by
        simp only [Real.exp_add]

      _ = _ := by
        rw [pow_two,← Real.exp_add]
        congr 1
        ring

  rw [Real.cosh_eq]

  linear_combination h1+h2

theorem rapidityRadial_separation
    (p q : Plane) (eta : ℝ)
    (hp : 0 < p.2) (hq : 0 < q.2) :
    radialSeparation
      (rapidityRadial p)
      (rapidityRadial q)
      (-relativeCos p.2 q.2 eta) =
      (Real.exp (-p.1))^2 +
      (Real.exp (-q.1))^2 -
      2*(Real.exp (-p.1) *
        Real.exp (-q.1)) *
        Real.cosh eta := by

  have hd :
      Real.sinh p.2*Real.sinh q.2 ≠ 0 :=
    mul_ne_zero
      (Real.sinh_pos_iff.mpr hp).ne'
      (Real.sinh_pos_iff.mpr hq).ne'

  have hc :
      Real.sinh p.2*Real.sinh q.2 *
        (-relativeCos p.2 q.2 eta) =
      Real.cosh p.2*Real.cosh q.2 -
        Real.cosh eta := by

    unfold relativeCos
    field_simp [hd] <;> ring

  rw [rapidityRadial_coordinates,
    rapidityRadial_coordinates]

  unfold radialSeparation
  dsimp only

  calc
    _ =
      (Real.exp (-p.1))^2 *
        (Real.cosh p.2^2-Real.sinh p.2^2) +
      (Real.exp (-q.1))^2 *
        (Real.cosh q.2^2-Real.sinh q.2^2) -
      2*(Real.exp (-p.1) *
        Real.exp (-q.1)) *
        (Real.cosh p.2*Real.cosh q.2 -
          Real.sinh p.2*Real.sinh q.2 *
            (-relativeCos p.2 q.2 eta)) := by
      ring

    _ = _ := by
      rw [Real.cosh_sq_sub_sinh_sq,
        Real.cosh_sq_sub_sinh_sq,hc]
      ring

theorem rapidity_spacelike_iff
    (p q : Plane) (eta : ℝ)
    (hp : 0 < p.2) (hq : 0 < q.2)
    (heta : 0 ≤ eta) :
    radialSeparation
      (rapidityRadial p)
      (rapidityRadial q)
      (-relativeCos p.2 q.2 eta) < 0 ↔
      |p.1-q.1| < eta := by

  rw [rapidityRadial_separation
    p q eta hp hq]

  rw [← exp_cosh_difference p.1 q.1]

  have hpos :
      0 < 2*(Real.exp (-p.1) *
        Real.exp (-q.1)) := by
    positivity

  have he :
      (2*(Real.exp (-p.1) *
        Real.exp (-q.1))) *
          Real.cosh (p.1-q.1) -
      (2*(Real.exp (-p.1) *
        Real.exp (-q.1))) *
          Real.cosh eta =
      (2*(Real.exp (-p.1) *
        Real.exp (-q.1))) *
        (Real.cosh (p.1-q.1) -
          Real.cosh eta) := by
    ring

  have hm :
      (2*(Real.exp (-p.1) *
        Real.exp (-q.1))) *
        (Real.cosh (p.1-q.1) -
          Real.cosh eta) < 0 ↔
      Real.cosh (p.1-q.1) -
        Real.cosh eta < 0 := by

    constructor

    · intro h
      apply lt_of_not_ge
      intro hn
      exact (not_lt_of_ge
        (mul_nonneg hpos.le hn)) h

    · intro h
      exact mul_neg_of_pos_of_neg hpos h

  rw [he,hm,sub_neg,
    Real.cosh_lt_cosh,
    abs_of_nonneg heta]

theorem negative_cosine_integral
    (x z : ℝ)
    (hx : 0 < x) (hz : 0 < z)
    (F : ℝ → ℝ≥0∞) :
    (∫⁻ c in Ioo (-1 : ℝ) 1,F c) =
      ∫⁻ eta in Ioo |x-z| (x+z),
        ENNReal.ofReal
          (Real.sinh eta /
            (Real.sinh x*Real.sinh z)) *
          F (-relativeCos x z eta) := by

  have himage :
      (fun c : ℝ => -c) ''
        Ioo (-1 : ℝ) 1 =
        Ioo (-1 : ℝ) 1 := by

    ext c
    constructor

    · rintro ⟨d,hd,rfl⟩
      exact ⟨by linarith [hd.2],
        by linarith [hd.1]⟩

    · intro hc
      exact ⟨-c,
        ⟨by linarith [hc.2],
          by linarith [hc.1]⟩,
        neg_neg c⟩

  have hd :
      ∀ c ∈ Ioo (-1 : ℝ) 1,
        HasDerivWithinAt
          (fun d : ℝ => -d) (-1)
          (Ioo (-1 : ℝ) 1) c := by
    intro c hc
    exact (hasDerivAt_id c).neg.hasDerivWithinAt

  have hi :
      InjOn (fun c : ℝ => -c)
        (Ioo (-1 : ℝ) 1) := by
    intro a ha b hb hab
    exact neg_injective hab

  have hs :=
    lintegral_image_eq_lintegral_abs_deriv_mul
      measurableSet_Ioo hd hi F

  rw [himage] at hs

  have hneg :
      (∫⁻ c in Ioo (-1 : ℝ) 1,F c) =
        ∫⁻ c in Ioo (-1 : ℝ) 1,
          F (-c) := by
    simpa using hs

  calc
    _ = ∫⁻ c in Ioo (-1 : ℝ) 1,
        F (-c) := hneg

    _ = _ :=
      relative_rapidity_lintegral
        x z hx hz (fun c => F (-c))

theorem spacelikeRadialKernel_explicit
    (p q : Plane) (eta : ℝ)
    (hp : 0 < p.2) (hq : 0 < q.2)
    (heta : 0 < eta) :
    spacelikeRadialKernel
      (rapidityRadial p,
        (rapidityRadial q,
          -relativeCos p.2 q.2 eta)) =
      if |p.1-q.1| < eta then
        (rapidityMassFormula
          p.1 q.1 eta)^2
      else 0 := by

  let P := radialProperSq
    (rapidityRadial p)

  let R := radialProperSq
    (rapidityRadial q)

  let S := radialSeparation
    (rapidityRadial p)
    (rapidityRadial q)
    (-relativeCos p.2 q.2 eta)

  have hP :
      P = (Real.exp (-p.1))^2 :=
    rapidityRadial_proper p

  have hR :
      R = (Real.exp (-q.1))^2 :=
    rapidityRadial_proper q

  have hS :
      S =
        (Real.exp (-p.1))^2 +
        (Real.exp (-q.1))^2 -
        2*(Real.exp (-p.1) *
          Real.exp (-q.1)) *
          Real.cosh eta :=
    rapidityRadial_separation
      p q eta hp hq

  have hsp :
      S < 0 ↔ |p.1-q.1| < eta :=
    rapidity_spacelike_iff
      p q eta hp hq heta.le

  change
    (if S < 0 then
      (massFromInvariants P R S)^2
    else 0) = _

  by_cases hs : S < 0

  · have hcond := hsp.mp hs

    rw [if_pos hs,if_pos hcond]

    have hp0 : 0 < P := by
      rw [hP]
      positivity

    have hq0 : 0 < R := by
      rw [hR]
      positivity

    have hl : logRadius P = p.1 := by
      unfold logRadius
      rw [hP,
        Real.sqrt_sq (Real.exp_pos _).le,
        Real.log_exp,neg_neg]

    have hm : logRadius R = q.1 := by
      unfold logRadius
      rw [hR,
        Real.sqrt_sq (Real.exp_pos _).le,
        Real.log_exp,neg_neg]

    have hc :
        invariantCos P R S =
          Real.cosh eta := by

      unfold invariantCos

      rw [hP,hR,hS,
        Real.sqrt_sq (Real.exp_pos _).le,
        Real.sqrt_sq (Real.exp_pos _).le]

      field_simp [
        (Real.exp_pos (-p.1)).ne',
        (Real.exp_pos (-q.1)).ne'] <;> ring

    obtain ⟨he0,hec⟩ :=
      invariant_relative_rapidity
        P R S hp0 hq0 hs

    rw [hc] at hec

    have ha :
        |relativeEta P R S| = |eta| :=
      le_antisymm
        (Real.cosh_le_cosh.mp hec.le)
        (Real.cosh_le_cosh.mp hec.ge)

    have he : relativeEta P R S = eta := by
      simpa only [
        abs_of_pos he0,
        abs_of_pos heta] using ha

    unfold massFromInvariants
    rw [hl,hm,he]

  · have hn : ¬ |p.1-q.1| < eta :=
      fun h => hs (hsp.mpr h)

    rw [if_neg hs,if_neg hn]

def explicitRelativeIntegral
    (p q : Plane) : ℝ≥0∞ :=
  ∫⁻ eta in Ioo |p.2-q.2| (p.2+q.2),
    ENNReal.ofReal
      (Real.sinh eta /
        (Real.sinh p.2*Real.sinh q.2)) *
      (if |p.1-q.1| < eta then
        (rapidityMassFormula
          p.1 q.1 eta)^2
      else 0)

theorem spacelike_angular_evaluation
    (p q : Plane)
    (hp : 0 < p.2)
    (hq : 0 < q.2) :
    jointAngularAverage spacelikeRadialKernel
      (rapidityRadial p,rapidityRadial q) =
      ENNReal.ofReal (1/2 : ℝ) *
        explicitRelativeIntegral p q := by

  unfold jointAngularAverage angularAverage
    explicitRelativeIntegral

  dsimp only

  congr 1

  calc
    _ =
      ∫⁻ eta in Ioo |p.2-q.2| (p.2+q.2),
        ENNReal.ofReal
          (Real.sinh eta /
            (Real.sinh p.2*Real.sinh q.2)) *
          spacelikeRadialKernel
            (rapidityRadial p,
              (rapidityRadial q,
                -relativeCos p.2 q.2 eta)) :=
      negative_cosine_integral
        p.2 q.2 hp hq
        (fun c =>
          spacelikeRadialKernel
            (rapidityRadial p,
              (rapidityRadial q,c)))

    _ = _ := by
      apply setLIntegral_congr_fun
        measurableSet_Ioo

      intro eta heta

      have he0 : 0 < eta :=
        lt_of_le_of_lt
          (abs_nonneg _) heta.1

      dsimp only

      rw [spacelikeRadialKernel_explicit
        p q eta hp hq he0]

theorem spacelikeMoment_explicit_integral :
    spacelikeMoment =
      ENNReal.ofReal (16 : ℝ) *
        ∫⁻ p in rapidityRegion,
          rapidityWeight p *
            (ENNReal.ofReal (16 : ℝ) *
              ∫⁻ q in rapidityRegion,
                rapidityWeight q *
                  (ENNReal.ofReal (1/2 : ℝ) *
                    explicitRelativeIntegral p q)) := by

  rw [spacelikeMoment_joint_reduction]

  congr 1

  have hregion : MeasurableSet rapidityRegion := by

    unfold rapidityRegion

    exact
      (isOpen_lt
        (f := fun _ : Plane => (0:ℝ))
        (g := fun p : Plane => p.2)
        continuous_const
        continuous_snd).measurableSet.inter
      (isOpen_lt
        (f := fun p : Plane => p.2)
        (g := fun p : Plane => p.1)
        continuous_snd
        continuous_fst).measurableSet

  apply setLIntegral_congr_fun hregion
  intro p hp

  dsimp only [secondRapidityAverage]

  congr 1
  congr 1

  apply setLIntegral_congr_fun hregion
  intro q hq

  have hp0 : 0 < p.2 := hp.1
  have hq0 : 0 < q.2 := hq.1

  dsimp only

  rw [spacelike_angular_evaluation
    p q hp0 hq0]

#print axioms rapidityRadial_coordinates
#print axioms rapidityRadial_proper
#print axioms rapidityRadial_separation
#print axioms rapidity_spacelike_iff
#print axioms negative_cosine_integral
#print axioms spacelikeRadialKernel_explicit
#print axioms spacelike_angular_evaluation
#print axioms spacelikeMoment_explicit_integral

end

end Chronos.FourEvent
