import LorentzBase
import CommonFutureVolume

open Set MeasureTheory
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

open Chronos.MinkowskiSimilarity
open Chronos.MinkowskiDiamond
open Chronos.MinkowskiVolume

private theorem weak_boost_forward
    (w x : Space) (t : ℝ)
    (hw : ‖w‖ < 1)
    (hx : ‖x‖ ≤ t) :
    ‖boostSpace w t x‖ ≤ boostTime w t x := by
  have ht : 0 ≤ t :=
    (norm_nonneg x).trans hx
  have hi :
      -(‖w‖*‖x‖) ≤ ⟪w,x⟫_ℝ :=
    (abs_le.mp
      (abs_real_inner_le_norm w x)).1
  have hm :=
    mul_nonneg (norm_nonneg w)
      (sub_nonneg.mpr hx)
  have hp :=
    mul_nonneg (sq_nonneg (1-‖w‖)) ht
  have htime : 0 ≤ boostTime w t x := by
    unfold boostTime
    nlinarith only [hi,hm,hp]
  apply
    (sq_le_sq₀
      (norm_nonneg (boostSpace w t x))
      htime).mp
  apply sub_nonneg.mp
  rw [lorentz_square]
  exact mul_nonneg
    (sq_nonneg (1-‖w‖^2))
    (sub_nonneg.mpr
      ((sq_le_sq₀ (norm_nonneg x) ht).mpr hx))

theorem weak_boost_future_iff
    (w x : Space) (t : ℝ)
    (hw : ‖w‖ < 1) :
    ‖boostSpace w t x‖ ≤ boostTime w t x ↔
      ‖x‖ ≤ t := by
  constructor
  · intro h
    have hi :=
      weak_boost_forward (-w)
        (boostSpace w t x)
        (boostTime w t x)
        (by simpa using hw) h
    rw [inverse_space, inverse_time,
      norm_smul, Real.norm_eq_abs,
      abs_of_nonneg (sq_nonneg _)] at hi
    have hk : 0 < (1-‖w‖^2)^2 :=
      k_pos w hw
    by_contra! hn
    have hbad := mul_pos hk (sub_pos.mpr hn)
    nlinarith only [hi, hbad]
  · exact weak_boost_forward w x t hw

def threeLens (x y z : Event) : Set Event :=
  {p | Precedes x p ∧ Precedes y p ∧ Precedes p z}

noncomputable def normalizedBoost
    (w : Space) : Event →ₗ[ℝ] Event :=
  (1-‖w‖^2)⁻¹ • L w

theorem lens_volume_transport
    (w : Space) (hw : ‖w‖ < 1)
    (d x y z : Event) :
    (volume : Measure Event)
      (threeLens
        (normalizedBoost w x+d)
        (normalizedBoost w y+d)
        (normalizedBoost w z+d)) =
      volume (threeLens x y z) := by
  letI : (volume : Measure Event).IsAddHaarMeasure := by
    rw [Measure.volume_eq_prod]
    infer_instance
  have hd : 0 < 1-‖w‖^2 := by
    have h :=
      mul_pos (sub_pos.mpr hw)
        (show 0 < 1+‖w‖ by
          linarith [norm_nonneg w])
    nlinarith only [h]
  let c := (1-‖w‖^2)⁻¹
  have hc : 0 < c := inv_pos.mpr hd
  let M : Event →ₗ[ℝ] Event := c • L w
  let F : Event → Event := fun p => M p+d

  have hdet : |LinearMap.det M| = 1 := by
    change |LinearMap.det (c • L w)| = 1
    rw [scaled_boost_abs_det w c hw hc]
    have h : c*(1-‖w‖^2) = 1 :=
      inv_mul_cancel₀ (ne_of_gt hd)
    rw [h,one_pow]

  have hord (p q : Event) :
      Precedes (F p) (F q) ↔ Precedes p q := by
    have he : F q-F p = M (q-p) := by
      dsimp [F]
      rw [map_sub]
      abel
    change
      ‖(F q-F p).2‖ ≤ (F q-F p).1 ↔
        ‖q.2-p.2‖ ≤ q.1-p.1
    rw [he]
    change
      ‖c • boostSpace w (q.1-p.1) (q.2-p.2)‖ ≤
        c * boostTime w (q.1-p.1) (q.2-p.2) ↔
          ‖q.2-p.2‖ ≤ q.1-p.1
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos hc]
    have hiff := weak_boost_future_iff w
      (q.2-p.2) (q.1-p.1) hw
    constructor
    · intro h
      apply hiff.mp
      by_contra! hn
      have hbad := mul_pos hc (sub_pos.mpr hn)
      nlinarith only [h, hbad]
    · intro h
      exact mul_le_mul_of_nonneg_left
        (hiff.mpr h) hc.le

  let e := scaledEquiv w c hw hc

  have hsurj : Function.Surjective F := by
    intro q
    refine ⟨e.symm (q-d),?_⟩
    change e (e.symm (q-d))+d = q
    rw [e.apply_symm_apply]
    abel

  have hpre :
      F ⁻¹' threeLens (F x) (F y) (F z) =
        threeLens x y z := by
    ext p
    change
      (Precedes (F x) (F p) ∧
        Precedes (F y) (F p) ∧
        Precedes (F p) (F z)) ↔
      (Precedes x p ∧ Precedes y p ∧ Precedes p z)
    simp only [hord]

  have himage :
      F '' threeLens x y z =
        threeLens (F x) (F y) (F z) := by
    rw [← hpre]
    exact Set.image_preimage_eq _ hsurj

  have htrans :
      F '' threeLens x y z =
        (fun p : Event => p+(-d)) ⁻¹'
          (M '' threeLens x y z) := by
    ext p
    constructor
    · rintro ⟨q,hq,rfl⟩
      exact ⟨q,hq,by dsimp [F]; abel⟩
    · intro hp
      change p+(-d) ∈ M '' threeLens x y z at hp
      obtain ⟨q,hq,he⟩ := hp
      refine ⟨q,hq,?_⟩
      change M q+d = p
      rw [he]
      abel

  change
    (volume : Measure Event)
      (threeLens (F x) (F y) (F z)) =
      volume (threeLens x y z)
  calc
    _ = volume (F '' threeLens x y z) := by
      rw [himage]
    _ = volume (M '' threeLens x y z) := by
      rw [htrans,measure_preimage_add_right]
    _ = ENNReal.ofReal |LinearMap.det M| *
          volume (threeLens x y z) :=
      Measure.addHaar_image_linearMap volume M _
    _ = _ := by rw [hdet,ENNReal.ofReal_one,one_mul]

#print axioms weak_boost_future_iff
#print axioms lens_volume_transport

end Chronos.FourEvent
