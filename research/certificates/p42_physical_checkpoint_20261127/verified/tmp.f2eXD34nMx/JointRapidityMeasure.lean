import PhysicalAngularRapidity

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

open Chronos.NullCoordinates

noncomputable section

abbrev JointInput := Plane × AngularInput

def spatialDirection (p : Event) : Space :=
  ‖p.2‖⁻¹ • p.2

theorem spatialDirection_unit
    (p : Event)
    (hp : p.2 ≠ 0) :
    ‖spatialDirection p‖ = 1 := by

  have hn : 0 < ‖p.2‖ :=
    norm_pos_iff.mpr hp

  unfold spatialDirection

  rw [norm_smul,Real.norm_eq_abs,
    abs_inv,
    abs_of_nonneg (norm_nonneg p.2),
    inv_mul_cancel₀ hn.ne']

theorem spatial_nonzero_ae :
    ∀ᵐ p : Event ∂uniform,
      p.2 ≠ 0 := by

  let S : Set Event :=
    (univ : Set ℝ) ×ˢ ({0} : Set Space)

  have hS : MeasurableSet S := by
    unfold S
    exact MeasurableSet.univ.prod
      (measurableSet_singleton 0)

  have hvol :
      (volume : Measure Event) S = 0 := by

    unfold S

    rw [Measure.volume_eq_prod,
      Measure.prod_prod]

    simp

  have hnull :
      uniform S = 0 := by

    unfold uniform

    rw [Measure.smul_apply,
      Measure.restrict_apply hS]

    have hi :
        (volume : Measure Event)
          (S ∩ diamond) = 0 :=
      measure_mono_null
        inter_subset_left hvol

    rw [hi,smul_eq_mul,mul_zero]

  have h :=
    measure_eq_zero_iff_ae_notMem.mp hnull

  filter_upwards [h] with p hp

  intro hz
  apply hp
  exact ⟨mem_univ _,by simpa [hz]⟩

def rapidityRadial (q : Plane) : Plane :=
  nullInverse (rapidityNull q)

theorem rapidityRadial_measurable :
    Measurable rapidityRadial := by

  change Measurable
    (fun q : Plane =>
      (1-(Real.exp (-q.1-q.2) +
          Real.exp (-q.1+q.2))/2,
       (Real.exp (-q.1+q.2) -
          Real.exp (-q.1-q.2))/2))

  fun_prop

def rapidityWeight (q : Plane) : ℝ≥0∞ :=
  ENNReal.ofReal (2*Real.exp (-2*q.1)) *
    Chronos.RadialMeasure.density
      (rapidityRadial q).2

theorem rapidityWeight_measurable :
    Measurable rapidityWeight := by

  have hd :
      Measurable
        Chronos.RadialMeasure.density := by
    unfold Chronos.RadialMeasure.density
    fun_prop

  have h :
      Measurable
        (fun q : Plane =>
          ENNReal.ofReal
            (2*Real.exp (-2*q.1))) := by
    fun_prop

  exact h.mul
    (hd.comp
      (measurable_snd.comp
        rapidityRadial_measurable))

theorem uniform_radial_rapidity
    (g : Plane → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p : Event,
      g (p.1,‖p.2‖) ∂uniform) =
      ENNReal.ofReal (16 : ℝ) *
        ∫⁻ q in rapidityRegion,
          rapidityWeight q *
            g (rapidityRadial q) := by

  have hd :
      diamond =
        Chronos.MinkowskiDiamond.diamond
          (0 : Event)
          Chronos.MinkowskiDiamond.tip := by

    ext p

    change
      (‖p.2‖ < p.1 ∧
        ‖p.2‖ < 1-p.1) ↔
      (‖p.2-0‖ < p.1-0 ∧
        ‖(0:Space)-p.2‖ < 1-p.1)

    simp

  have hdim :
      Module.finrank ℝ Space = 3 := by
    simp [Space]

  have h :=
    normalized_physical_rapidity_integral
      (volume : Measure Space)
      hdim g hg

  rw [← hd,
    ← Measure.volume_eq_prod,
    Chronos.GeometricTransport.normalized,
    Measure.restrict_apply_univ] at h

  calc
    _ = ENNReal.ofReal (16 : ℝ) *
        (∫⁻ q in rapidityRegion,
          ENNReal.ofReal
            (2*Real.exp (-2*q.1)) *
            (Chronos.RadialMeasure.density
              (rapidityRadial q).2 *
                g (rapidityRadial q))) := h

    _ = _ := by
      congr 1
      apply lintegral_congr
      intro q
      unfold rapidityWeight
      ac_rfl

def jointAngularAverage
    (F : JointInput → ℝ≥0∞)
    (p : Plane × Plane) : ℝ≥0∞ :=
  angularAverage
    (fun a => F (p.1,a))
    p.2

theorem jointAngularAverage_measurable
    (F : JointInput → ℝ≥0∞)
    (hF : Measurable F) :
    Measurable (jointAngularAverage F) := by

  let H : (Plane × Plane) × ℝ → ℝ≥0∞ :=
    fun a => F
      (a.1.1,(a.1.2,a.2))

  have hH : Measurable H := by
    unfold H
    fun_prop

  have hm :
      Measurable
        (fun p : Plane × Plane =>
          ∫⁻ c in Ioo (-1 : ℝ) 1,
            H (p,c)) :=
    Measurable.lintegral_prod_right'
      (ν := (volume : Measure ℝ).restrict
        (Ioo (-1 : ℝ) 1))
      hH

  exact measurable_const.mul hm

def secondRapidityAverage
    (F : JointInput → ℝ≥0∞)
    (p : Plane) : ℝ≥0∞ :=
  ENNReal.ofReal (16 : ℝ) *
    ∫⁻ q in rapidityRegion,
      rapidityWeight q *
        jointAngularAverage F
          (p,rapidityRadial q)

theorem secondRapidityAverage_measurable
    (F : JointInput → ℝ≥0∞)
    (hF : Measurable F) :
    Measurable (secondRapidityAverage F) := by

  let K : Plane × Plane → ℝ≥0∞ :=
    fun p =>
      rapidityWeight p.2 *
        jointAngularAverage F
          (p.1,rapidityRadial p.2)

  have hK : Measurable K :=
    (rapidityWeight_measurable.comp
      measurable_snd).mul
      ((jointAngularAverage_measurable
        F hF).comp
        (measurable_fst.prodMk
          (rapidityRadial_measurable.comp
            measurable_snd)))

  have hm :
      Measurable
        (fun p : Plane =>
          ∫⁻ q in rapidityRegion,
            K (p,q)) :=
    Measurable.lintegral_prod_right'
      (ν := (volume : Measure Plane).restrict
        rapidityRegion)
      hK

  exact measurable_const.mul hm

theorem joint_physical_rapidity_integral
    (F : JointInput → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ x : Event,
      ∫⁻ y : Event,
        F
          ((x.1,‖x.2‖),
            ((y.1,‖y.2‖),
              ⟪spatialDirection x,y.2⟫_ℝ /
                ‖y.2‖))
        ∂uniform ∂uniform) =
      ENNReal.ofReal (16 : ℝ) *
        ∫⁻ p in rapidityRegion,
          rapidityWeight p *
            secondRapidityAverage F
              (rapidityRadial p) := by

  calc
    _ = ∫⁻ x : Event,
        secondRapidityAverage F
          (x.1,‖x.2‖) ∂uniform := by

      apply lintegral_congr_ae

      filter_upwards [spatial_nonzero_ae]
        with x hx

      let G : AngularInput → ℝ≥0∞ :=
        fun a => F ((x.1,‖x.2‖),a)

      have hG : Measurable G := by
        unfold G
        fun_prop

      have h :=
        physical_angular_rapidity_integral
          (spatialDirection x)
          (spatialDirection_unit x hx)
          G hG

      calc
        _ = ENNReal.ofReal (16 : ℝ) *
            (∫⁻ q in rapidityRegion,
              ENNReal.ofReal
                (2*Real.exp (-2*q.1)) *
                (Chronos.RadialMeasure.density
                  (rapidityRadial q).2 *
                    angularAverage G
                      (rapidityRadial q))) := h

        _ = _ := by

          unfold secondRapidityAverage

          congr 1

          apply lintegral_congr
          intro q

          have he :
              angularAverage G
                (rapidityRadial q) =
              jointAngularAverage F
                ((x.1,‖x.2‖),rapidityRadial q) :=
            rfl

          rw [he]

          unfold rapidityWeight

          ac_rfl

    _ = _ :=
      uniform_radial_rapidity
        (secondRapidityAverage F)
        (secondRapidityAverage_measurable
          F hF)

#print axioms spatialDirection_unit
#print axioms spatial_nonzero_ae
#print axioms rapidityRadial_measurable
#print axioms rapidityWeight_measurable
#print axioms uniform_radial_rapidity
#print axioms jointAngularAverage_measurable
#print axioms secondRapidityAverage_measurable
#print axioms joint_physical_rapidity_integral

end

end Chronos.FourEvent
