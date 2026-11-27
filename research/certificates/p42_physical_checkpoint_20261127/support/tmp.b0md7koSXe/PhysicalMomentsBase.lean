import LorentzBase
open MeasureTheory Set
open scoped ENNReal NNReal InnerProductSpace Interval



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
