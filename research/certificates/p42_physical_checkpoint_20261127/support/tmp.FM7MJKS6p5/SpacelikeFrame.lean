import AxialVolumeExact
import LensTransport
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection

open Set MeasureTheory
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

open Chronos.MinkowskiSimilarity
open Chronos.MinkowskiDiamond
open Chronos.MinkowskiVolume

noncomputable section

def invariantSq (p : Event) : ℝ :=
  p.1^2-‖p.2‖^2

abbrev StrictBefore :=
  @Chronos.MinkowskiDiamond.precedes Space _

private theorem boost_den_pos
    (w : Space) (hw : ‖w‖ < 1) :
    0 < 1-‖w‖^2 := by
  have h := mul_pos (sub_pos.mpr hw)
    (show 0 < 1+‖w‖ by
      linarith [norm_nonneg w])
  nlinarith only [h]

theorem normalizedBoost_sq
    (w : Space) (hw : ‖w‖ < 1)
    (p : Event) :
    invariantSq (normalizedBoost w p) =
      invariantSq p := by
  have hd := boost_den_pos w hw
  change
    ((1-‖w‖^2)⁻¹*boostTime w p.1 p.2)^2 -
      ‖(1-‖w‖^2)⁻¹ • boostSpace w p.1 p.2‖^2 =
        p.1^2-‖p.2‖^2
  rw [norm_smul,Real.norm_eq_abs,
    abs_of_pos (inv_pos.mpr hd)]
  calc
    _ = ((1-‖w‖^2)⁻¹)^2 *
        ((boostTime w p.1 p.2)^2 -
          ‖boostSpace w p.1 p.2‖^2) := by ring
    _ = _ := by
      rw [lorentz_square]
      field_simp [ne_of_gt hd] <;> ring

private def Frame (F : Event → Event) : Prop :=
  (∀ p q, invariantSq (F q-F p) =
      invariantSq (q-p)) ∧
  (∀ p q, StrictBefore (F p) (F q) ↔
      StrictBefore p q) ∧
  (∀ p q z, (volume : Measure Event)
      (threeLens (F p) (F q) (F z)) =
      volume (threeLens p q z))

private theorem frame_comp
    (F G : Event → Event)
    (hF : Frame F) (hG : Frame G) :
    Frame (G ∘ F) := by
  refine ⟨?_,?_,?_⟩
  · intro p q
    simp only [Function.comp_apply,hG.1,hF.1]
  · intro p q
    simp only [Function.comp_apply,hG.2.1,hF.2.1]
  · intro p q z
    simp only [Function.comp_apply,hG.2.2,hF.2.2]

private def boostAffine
    (w : Space) (d : Event) (p : Event) : Event :=
  normalizedBoost w p+d

private theorem boost_frame
    (w : Space) (hw : ‖w‖ < 1)
    (d : Event) :
    Frame (boostAffine w d) := by
  refine ⟨?_,?_,?_⟩
  · intro p q
    have h :
        boostAffine w d q-boostAffine w d p =
          normalizedBoost w (q-p) := by
      unfold boostAffine
      rw [map_sub]
      abel
    rw [h,normalizedBoost_sq w hw]
  · intro p q
    exact affine_precedes_iff w
      (1-‖w‖^2)⁻¹ hw
      (inv_pos.mpr (boost_den_pos w hw))
      d p q
  · exact lens_volume_transport w hw d

private theorem threeLens_measurable
    (x y z : Event) :
    MeasurableSet (threeLens x y z) := by
  change MeasurableSet
    ({p : Event | ‖p.2-x.2‖ ≤ p.1-x.1} ∩
      ({p : Event | ‖p.2-y.2‖ ≤ p.1-y.1} ∩
        {p : Event | ‖z.2-p.2‖ ≤ z.1-p.1}))
  apply MeasurableSet.inter
  · exact (isClosed_le (by fun_prop)
      (by fun_prop)).measurableSet
  · apply MeasurableSet.inter <;>
      exact (isClosed_le (by fun_prop)
        (by fun_prop)).measurableSet

private def spin
    (J : Space ≃ₗᵢ[ℝ] Space) (p : Event) : Event :=
  (p.1,J p.2)

private theorem spin_frame
    (J : Space ≃ₗᵢ[ℝ] Space) :
    Frame (spin J) := by
  have hweak (p q : Event) :
      Precedes (spin J p) (spin J q) ↔
        Precedes p q := by
    change ‖J q.2-J p.2‖ ≤ q.1-p.1 ↔
      ‖q.2-p.2‖ ≤ q.1-p.1
    rw [← map_sub,J.norm_map]
  have hmeasure : MeasurePreserving (spin J) := by
    refine ⟨?_,?_⟩
    · exact measurable_fst.prodMk
        (J.continuous.measurable.comp measurable_snd)
    · rw [Measure.volume_eq_prod]
      change Measure.map (Prod.map id J)
        ((volume : Measure ℝ).prod
          (volume : Measure Space)) =
        (volume : Measure ℝ).prod
          (volume : Measure Space)
      rw [← Measure.map_prod_map
        _ _ measurable_id J.continuous.measurable,
        Measure.map_id,J.measurePreserving.map_eq]
  refine ⟨?_,?_,?_⟩
  · intro p q
    change
      (q.1-p.1)^2-‖J q.2-J p.2‖^2 =
      (q.1-p.1)^2-‖q.2-p.2‖^2
    rw [← map_sub,J.norm_map]
  · intro p q
    change ‖J q.2-J p.2‖ < q.1-p.1 ↔
      ‖q.2-p.2‖ < q.1-p.1
    rw [← map_sub,J.norm_map]
  · intro x y z
    have hp :
        spin J ⁻¹'
          threeLens (spin J x) (spin J y) (spin J z) =
            threeLens x y z := by
      ext p
      change
        (Precedes (spin J x) (spin J p) ∧
          Precedes (spin J y) (spin J p) ∧
          Precedes (spin J p) (spin J z)) ↔
        (Precedes x p ∧ Precedes y p ∧ Precedes p z)
      simp only [hweak]
    rw [← hmeasure.measure_preimage
      (threeLens_measurable
        (spin J x) (spin J y) (spin J z)).nullMeasurableSet,
      hp]

private theorem boost_rest
    (p : Event) (hp : ‖p.2‖ < p.1) :
    ∃ w : Space, ‖w‖ < 1 ∧
      ∃ U : ℝ, 0 < U ∧
        normalizedBoost w p = (U,0) := by
  obtain ⟨c,w,hc,hw,ht,hs⟩ :=
    tip_reachable p.1 p.2 hp
  have hd := boost_den_pos w hw
  have hp' : p = c • B w (1,0) := by
    apply Prod.ext
    · exact ht.symm
    · exact hs.symm
  refine ⟨-w,by simpa using hw,
    c*(1-‖w‖^2),mul_pos hc hd,?_⟩
  rw [hp']
  change
    (1-‖-w‖^2)⁻¹ •
      B (-w) (c • B w (1,0)) =
        (c*(1-‖w‖^2),0)
  rw [norm_neg,B_smul,B_neg_comp,
    smul_smul,smul_smul]
  have hfactor :
      ((1-‖w‖^2)⁻¹*c)*k w =
        c*(1-‖w‖^2) := by
    unfold k
    field_simp [ne_of_gt hd] <;> ring
  rw [hfactor]
  simp

private theorem axis_norm (c : ℝ) :
    ‖axis c‖ = |c| := by
  simp [axis,PiLp.norm_single,Real.norm_eq_abs]

private theorem axis_zero :
    axis 0 = 0 := by
  ext i
  simp [axis]

private theorem axis_add (c d : ℝ) :
    axis (c+d) = axis c+axis d := by
  ext i
  by_cases hi : i = 0 <;>
    simp [axis,hi]

private theorem axis_sub (c d : ℝ) :
    axis (c-d) = axis c-axis d := by
  ext i
  by_cases hi : i = 0 <;>
    simp [axis,hi]

private theorem axis_neg (c : ℝ) :
    axis (-c) = -axis c := by
  ext i
  by_cases hi : i = 0 <;>
    simp [axis,hi]

private theorem axis_smul (c d : ℝ) :
    c • axis d = axis (c*d) := by
  ext i
  by_cases hi : i = 0 <;>
    simp [axis,hi,smul_eq_mul]

private theorem axis_inner (c d : ℝ) :
    ⟪axis c,axis d⟫_ℝ = c*d := by
  change
    ⟪EuclideanSpace.single (0 : Fin 3) c,
      axis d⟫_ℝ = c*d
  rw [EuclideanSpace.inner_single_left]
  simp [axis]

private theorem boost_axis (j t x : ℝ) :
    normalizedBoost (axis j) (t,axis x) =
      (((1+j^2)*t+2*j*x)/(1-j^2),
        axis (((1+j^2)*x+2*j*t)/(1-j^2))) := by
  apply Prod.ext
  · change
      (1-‖axis j‖^2)⁻¹ *
        boostTime (axis j) t (axis x) =
          ((1+j^2)*t+2*j*x)/(1-j^2)
    rw [boostTime,axis_norm,sq_abs,axis_inner]
    ring
  · change
      (1-‖axis j‖^2)⁻¹ •
        boostSpace (axis j) t (axis x) =
          axis (((1+j^2)*x+2*j*t)/(1-j^2))
    rw [boostSpace,axis_norm,sq_abs,axis_inner,
      axis_smul,axis_smul,← axis_add,axis_smul]
    apply congrArg axis
    ring

private theorem invariant_neg (p : Event) :
    invariantSq (-p) = invariantSq p := by
  change (-p.1)^2-‖-p.2‖^2 =
    p.1^2-‖p.2‖^2
  rw [norm_neg]
  ring

private theorem centered_axial_frame
    (q : Event) (U : ℝ)
    (hU : 0 < U)
    (hspace : invariantSq q < 0)
    (hs : q.1 ≤ 0)
    (hx : StrictBefore (-q) (U,0))
    (hy : StrictBefore q (U,0)) :
    ∃ F : Event → Event,
      ∃ a b T : ℝ,
        Frame F ∧ 0 < a ∧ 0 ≤ b ∧ a+b < T ∧
        F (-q) = (0,axis (-a)) ∧
        F q = (0,axis a) ∧
        F (U,0) = (T,axis b) := by
  let r := ‖q.2‖
  let s := q.1
  have hsr : s^2 < r^2 := by
    change s^2-r^2 < 0 at hspace
    linarith
  have hr : 0 < r := by
    have hr0 : 0 ≤ r := norm_nonneg _
    by_contra! hn
    have he : r = 0 := le_antisymm hn hr0
    rw [he] at hsr
    nlinarith [sq_nonneg s]
  have habs : |s| < r := by
    by_contra! hn
    have hh :=
      (sq_le_sq₀ hr.le (abs_nonneg s)).mpr hn
    rw [sq_abs] at hh
    linarith
  let a := Real.sqrt (r^2-s^2)
  have ha : 0 < a :=
    Real.sqrt_pos.2 (sub_pos.mpr hsr)
  have ha2 : a^2 = r^2-s^2 :=
    Real.sq_sqrt (sub_nonneg.mpr hsr.le)
  have hra : 0 < r+a := add_pos hr ha
  let j := s/(r+a)
  have hjrel : j*(r+a) = s := by
    dsimp [j]
    field_simp [ne_of_gt hra]
  have hjabs : |j| < 1 := by
    dsimp [j]
    rw [abs_div,abs_of_pos hra]
    apply (div_lt_iff₀ hra).mpr
    linarith
  have hjnonpos : j ≤ 0 :=
    div_nonpos_of_nonpos_of_nonneg hs hra.le
  have hj2 : j^2*(r+a) = r-a := by
    have hh := congrArg (fun v : ℝ => v^2) hjrel
    have hprod :
        (r+a)*(j^2*(r+a)-(r-a)) = 0 := by
      nlinarith only [hh,ha2]
    exact sub_eq_zero.mp
      ((mul_eq_zero.mp hprod).resolve_left
        (ne_of_gt hra))
  have hjs : j*s = r-a := by
    have hh := congrArg (fun v : ℝ => j*v) hjrel
    nlinarith only [hh,hj2]
  have htime :
      (1+j^2)*s-2*j*r = 0 := by
    have hh :=
      congrArg (fun v : ℝ => j*v) hjs
    nlinarith only [hjrel,hh]
  have haxial :
      (1+j^2)*r-2*j*s = a*(1-j^2) := by
    nlinarith only [hj2,hjs]
  have hw : ‖axis (-j)‖ < 1 := by
    rw [axis_norm,abs_neg]
    exact hjabs
  have hd : 0 < 1-j^2 := by
    have hh := boost_den_pos (axis (-j)) hw
    rw [axis_norm,sq_abs,neg_sq] at hh
    exact hh

  have hnorm : ‖q.2‖ = ‖axis r‖ := by
    rw [axis_norm,abs_of_pos hr]

  let J : Space ≃ₗᵢ[ℝ] Space :=
    Submodule.reflection (ℝ ∙ (q.2-axis r))ᗮ

  have hJ : J q.2 = axis r :=
    Submodule.reflection_sub hnorm

  let T := (1+j^2)*U/(1-j^2)
  let b := (-2*j*U)/(1-j^2)

  have hb : 0 ≤ b := by
    dsimp [b]
    apply div_nonneg _ hd.le
    exact mul_nonneg
      (by linarith : 0 ≤ -2*j) hU.le

  let F := boostAffine (axis (-j)) 0 ∘ spin J
  have hF : Frame F :=
    frame_comp _ _ (spin_frame J)
      (boost_frame _ hw 0)

  have hq : F q = (0,axis a) := by
    change normalizedBoost (axis (-j))
      (s,J q.2)+0 = _
    rw [hJ,add_zero,boost_axis]
    apply Prod.ext
    · change
        ((1+(-j)^2)*s+2*(-j)*r)/
          (1-(-j)^2) = 0
      rw [neg_sq]
      have hh :
          (1+j^2)*s+2*(-j)*r = 0 := by
        nlinarith only [htime]
      rw [hh,zero_div]
    · apply congrArg axis
      rw [neg_sq]
      apply (div_eq_iff (ne_of_gt hd)).mpr
      nlinarith only [haxial]

  have hneg : F (-q) = (0,axis (-a)) := by
    have hh : F (-q) = -(F q) := by
      change
        normalizedBoost (axis (-j))
          (-s,J (-q.2))+0 =
        -(normalizedBoost (axis (-j))
          (s,J q.2)+0)
      rw [map_neg,add_zero,add_zero]
      change
        normalizedBoost (axis (-j))
          (-(s,J q.2)) =
        -(normalizedBoost (axis (-j))
          (s,J q.2))
      exact map_neg _ _
    rw [hh,hq]
    simp [axis_neg]

  have htop : F (U,0) = (T,axis b) := by
    change normalizedBoost (axis (-j))
      (U,J 0)+0 = _
    rw [map_zero,add_zero,← axis_zero,boost_axis]
    apply Prod.ext
    · dsimp [T]
      ring
    · apply congrArg axis
      dsimp [b]
      ring

  have hstrict := (hF.2.1 (-q) (U,0)).mpr hx
  rw [hneg,htop] at hstrict
  change ‖axis b-axis (-a)‖ < T-0 at hstrict
  rw [← axis_sub,axis_norm,
    abs_of_nonneg (by linarith : 0 ≤ b-(-a))] at hstrict

  exact ⟨F,a,b,T,hF,ha,hb,
    by linarith,hneg,hq,htop⟩

private theorem conclude_axial
    (F : Event → Event) (hF : Frame F)
    (x y z : Event) (a b T : ℝ)
    (ha : 0 < a) (hb : 0 ≤ b)
    (hT : a+b < T)
    (hx : F x = (0,axis (-a)))
    (hy : F y = (0,axis a))
    (hz : F z = (T,axis b)) :
    invariantSq (y-x) = -4*a^2 ∧
    invariantSq (z-x)+invariantSq (z-y) =
      2*(T^2-a^2-b^2) ∧
    (invariantSq (z-x)-invariantSq (z-y))^2 =
      16*a^2*b^2 ∧
    (volume : Measure Event) (threeLens x y z) =
      ENNReal.ofReal
        (Real.pi*(T+2*a)*((T-a)^2-b^2)^2/(24*T)) := by
  have hxy := hF.1 x y
  have hxz := hF.1 x z
  have hyz := hF.1 y z
  rw [hx,hy] at hxy
  rw [hx,hz] at hxz
  rw [hy,hz] at hyz
  change 0^2-‖axis a-axis (-a)‖^2 =
    invariantSq (y-x) at hxy
  change (T-0)^2-‖axis b-axis (-a)‖^2 =
    invariantSq (z-x) at hxz
  change (T-0)^2-‖axis b-axis a‖^2 =
    invariantSq (z-y) at hyz
  rw [← axis_sub,axis_norm,sq_abs] at hxy hxz hyz
  refine ⟨?_,?_,?_,?_⟩
  · nlinarith only [hxy]
  · nlinarith only [hxz,hyz]
  · rw [← hxz,← hyz]
    ring
  · have hv := hF.2.2 x y z
    rw [hx,hy,hz] at hv
    change (volume : Measure Event)
      (axialLens a b T) = volume (threeLens x y z) at hv
    rw [← hv]
    exact axialLens_volume_exact a b T ha hb hT

theorem spacelike_lens_volume_exact_invariants
    (x y z : Event)
    (hx : StrictBefore x z)
    (hy : StrictBefore y z)
    (hspace : invariantSq (y-x) < 0) :
    ∃ a b T : ℝ,
      0 < a ∧ 0 ≤ b ∧ a+b < T ∧
      invariantSq (y-x) = -4*a^2 ∧
      invariantSq (z-x)+invariantSq (z-y) =
        2*(T^2-a^2-b^2) ∧
      (invariantSq (z-x)-invariantSq (z-y))^2 =
        16*a^2*b^2 ∧
      (volume : Measure Event) (threeLens x y z) =
        ENNReal.ofReal
          (Real.pi*(T+2*a)*((T-a)^2-b^2)^2/(24*T)) := by
  let m : Event := (1/2 : ℝ) • (x+y)

  have hm : ‖(z-m).2‖ < (z-m).1 := by
    change ‖z.2-x.2‖ < z.1-x.1 at hx
    change ‖z.2-y.2‖ < z.1-y.1 at hy
    change
      ‖z.2-(1/2 : ℝ) • (x.2+y.2)‖ <
        z.1-(1/2)*(x.1+y.1)
    have he :
        z.2-(1/2 : ℝ) • (x.2+y.2) =
          (1/2 : ℝ) •
            ((z.2-x.2)+(z.2-y.2)) := by module
    rw [he,norm_smul,Real.norm_eq_abs,
      abs_of_nonneg (by norm_num : 0 ≤ (1/2 : ℝ))]
    linarith [norm_add_le (z.2-x.2) (z.2-y.2)]

  obtain ⟨w,hw,U,hU,hrest⟩ :=
    boost_rest (z-m) hm

  let F := boostAffine w (-(normalizedBoost w m))
  have hF : Frame F := boost_frame w hw _
  have hcenter (p : Event) :
      F p = normalizedBoost w (p-m) := by
    unfold F boostAffine
    rw [map_sub]
    abel

  let q := F y
  have hq : F y = q := rfl
  have hneg : F x = -q := by
    have h : x-m = -(y-m) := by
      dsimp [m]
      module
    rw [hcenter x,h,map_neg,← hcenter y]

  have htop : F z = (U,0) := by
    rw [hcenter,hrest]

  have hsq := hF.1 x y
  rw [hneg,hq] at hsq
  have he : q-(-q) = (2 : ℝ) • q := by module
  rw [he] at hsq

  have hscale :
      invariantSq ((2 : ℝ) • q) =
        4*invariantSq q := by
    change
      (2*q.1)^2-‖(2 : ℝ) • q.2‖^2 =
        4*(q.1^2-‖q.2‖^2)
    rw [norm_smul,Real.norm_eq_abs]
    norm_num <;> ring

  rw [hscale] at hsq

  have hqspace : invariantSq q < 0 := by
    linarith

  have hqx := (hF.2.1 x z).mpr hx
  have hqy := (hF.2.1 y z).mpr hy
  rw [hneg,htop] at hqx
  rw [hq,htop] at hqy

  by_cases hs : q.1 ≤ 0
  · obtain ⟨G,a,b,T,hG,ha,hb,hT,hGx,hGy,hGz⟩ :=
      centered_axial_frame q U hU hqspace hs hqx hqy
    refine ⟨a,b,T,ha,hb,hT,?_⟩
    exact conclude_axial (G ∘ F)
      (frame_comp F G hF hG)
      x y z a b T ha hb hT
      (by simpa only [Function.comp_apply,hneg] using hGx)
      (by simpa only [Function.comp_apply,hq] using hGy)
      (by simpa only [Function.comp_apply,htop] using hGz)
  · have hnspace : invariantSq (-q) < 0 := by
      rw [invariant_neg]
      exact hqspace
    have hns : (-q).1 ≤ 0 := by
      change -q.1 ≤ 0
      linarith [lt_of_not_ge hs]
    obtain ⟨G,a,b,T,hG,ha,hb,hT,hGx,hGy,hGz⟩ :=
      centered_axial_frame (-q) U hU hnspace hns
        (by simpa using hqy) hqx
    have hresult :=
      conclude_axial (G ∘ F)
        (frame_comp F G hF hG)
        y x z a b T ha hb hT
        (by simpa only [Function.comp_apply,hq,neg_neg]
          using hGx)
        (by simpa only [Function.comp_apply,hneg]
          using hGy)
        (by simpa only [Function.comp_apply,htop]
          using hGz)
    have hrev : invariantSq (x-y) =
        invariantSq (y-x) := by
      rw [show x-y = -(y-x) by abel,invariant_neg]
    have hcomm : threeLens y x z = threeLens x y z := by
      ext p
      change
        (Precedes y p ∧ Precedes x p ∧ Precedes p z) ↔
        (Precedes x p ∧ Precedes y p ∧ Precedes p z)
      tauto
    obtain ⟨h1,h2,h3,h4⟩ := hresult
    rw [hrev] at h1
    rw [hcomm] at h4
    refine ⟨a,b,T,ha,hb,hT,h1,?_ ,?_ ,h4⟩
    · linarith only [h2]
    · nlinarith only [h3]

#print axioms normalizedBoost_sq
#print axioms spacelike_lens_volume_exact_invariants

end

end Chronos.FourEvent
