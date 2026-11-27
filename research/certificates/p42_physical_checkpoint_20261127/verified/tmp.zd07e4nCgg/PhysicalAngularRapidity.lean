import RelativeRapidityMeasure
import PhysicalAngularIntegral

open MeasureTheory Set
open scoped ENNReal InnerProductSpace

namespace Chronos.FourEvent

noncomputable section

abbrev AngularInput := (ℝ × ℝ) × ℝ

def angularAverage
    (F : AngularInput → ℝ≥0∞)
    (p : ℝ × ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (1/2 : ℝ) *
    ∫⁻ c in Ioo (-1 : ℝ) 1,
      F (p,c)

theorem angularAverage_measurable
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F) :
    Measurable (angularAverage F) := by

  have h :
      Measurable
        (fun p : ℝ × ℝ =>
          ∫⁻ c in Ioo (-1 : ℝ) 1,
            F (p,c)) :=
    Measurable.lintegral_prod_right'
      (ν := (volume : Measure ℝ).restrict
        (Ioo (-1 : ℝ) 1))
      hF

  exact measurable_const.mul h

private def unitSpatialBall : Set Space :=
  {v | ‖v‖ < 1}

private theorem unitSpatialBall_measurable :
    MeasurableSet unitSpatialBall := by
  exact
    (isOpen_lt
      (f := fun v : Space => ‖v‖)
      (g := fun _ : Space => 1)
      continuous_norm
      continuous_const).measurableSet

private theorem eventDiamond_measurable :
    MeasurableSet diamond := by

  change MeasurableSet
    {p : Event |
      ‖p.2‖ < p.1 ∧
      ‖p.2‖ < 1-p.1}

  exact
    (isOpen_lt
      (f := fun p : Event => ‖p.2‖)
      (g := fun p : Event => p.1)
      (by fun_prop)
      (by fun_prop)).measurableSet.inter
    (isOpen_lt
      (f := fun p : Event => ‖p.2‖)
      (g := fun p : Event => 1-p.1)
      (by fun_prop)
      (by fun_prop)).measurableSet

private def angularSlice
    (F : AngularInput → ℝ≥0∞)
    (t : ℝ)
    (p : ℝ × ℝ) : ℝ≥0∞ :=
  if p.1 < t ∧ p.1 < 1-t then
    F ((t,p.1),p.2)
  else 0

private theorem angularSlice_measurable
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F)
    (t : ℝ) :
    Measurable (angularSlice F t) := by

  have hs :
      MeasurableSet
        {p : ℝ × ℝ |
          p.1 < t ∧ p.1 < 1-t} :=
    (isOpen_lt
      (f := fun p : ℝ × ℝ => p.1)
      (g := fun _ : ℝ × ℝ => t)
      continuous_fst
      continuous_const).measurableSet.inter
    (isOpen_lt
      (f := fun p : ℝ × ℝ => p.1)
      (g := fun _ : ℝ × ℝ => 1-t)
      continuous_fst
      continuous_const).measurableSet

  unfold angularSlice

  exact Measurable.ite hs
    (by fun_prop)
    measurable_const

private theorem diamond_angular_slices
    (e : Space)
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p in diamond,
      F ((p.1,‖p.2‖),
        ⟪e,p.2⟫_ℝ/‖p.2‖)) =
      ∫⁻ t : ℝ,
        ∫⁻ v in unitSpatialBall,
          angularSlice F t
            (‖v‖,⟪e,v⟫_ℝ/‖v‖) := by

  let H : Event → ℝ≥0∞ :=
    diamond.indicator
      (fun p =>
        F ((p.1,‖p.2‖),
          ⟪e,p.2⟫_ℝ/‖p.2‖))

  have hH : Measurable H := by
    unfold H
    apply Measurable.indicator _
      eventDiamond_measurable
    fun_prop

  calc
    _ = ∫⁻ p : Event,H p := by
      unfold H
      rw [lintegral_indicator
        eventDiamond_measurable]

    _ = ∫⁻ t : ℝ,
        ∫⁻ v : Space,H (t,v) := by

      rw [Measure.volume_eq_prod]
      exact lintegral_prod _
        hH.aemeasurable

    _ = _ := by

      apply lintegral_congr
      intro t

      rw [← lintegral_indicator
        unitSpatialBall_measurable]

      apply lintegral_congr
      intro v

      by_cases hv :
        ‖v‖ < t ∧ ‖v‖ < 1-t

      · have hd : (t,v) ∈ diamond := hv

        have hb : v ∈ unitSpatialBall := by
          change ‖v‖ < 1
          linarith [hv.1,hv.2]

        unfold H angularSlice

        rw [Set.indicator_of_mem hd,
          Set.indicator_of_mem hb]

        simp [hv]

      · have hd : (t,v) ∉ diamond := hv

        unfold H angularSlice

        rw [Set.indicator_of_notMem hd]

        by_cases hb : v ∈ unitSpatialBall

        · rw [Set.indicator_of_mem hb]
          simp [hv]

        · rw [Set.indicator_of_notMem hb]

private theorem angularSlice_average
    (F : AngularInput → ℝ≥0∞)
    (t r : ℝ) :
    (∫⁻ c in Ioo (-1 : ℝ) 1,
      angularSlice F t (r,c)) =
      ∫⁻ c in Ioo (-1 : ℝ) 1,
        angularSlice
          (fun p => angularAverage F p.1)
          t (r,c) := by

  by_cases hr : r < t ∧ r < 1-t

  · simp only [angularSlice,if_pos hr]

    rw [setLIntegral_const,
      Real.volume_Ioo]

    have hlen : (1:ℝ)-(-1) = 2 := by
      norm_num

    rw [hlen]

    unfold angularAverage

    have htwo :
        ENNReal.ofReal (2 : ℝ) *
          ENNReal.ofReal (1/2 : ℝ) = 1 := by

      rw [← ENNReal.ofReal_mul
        (by norm_num : (0:ℝ) ≤ 2)]

      norm_num

    calc
      _ = 1 *
          (∫⁻ c in Ioo (-1 : ℝ) 1,
            F ((t,r),c)) :=
        (one_mul _).symm

      _ = (ENNReal.ofReal (2 : ℝ) *
          ENNReal.ofReal (1/2 : ℝ)) *
          (∫⁻ c in Ioo (-1 : ℝ) 1,
            F ((t,r),c)) := by
        rw [htwo]

      _ = _ := by ac_rfl

  · simp [angularSlice,hr]

theorem physical_angular_average_raw
    (e : Space)
    (he : ‖e‖ = 1)
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p in diamond,
      F ((p.1,‖p.2‖),
        ⟪e,p.2⟫_ℝ/‖p.2‖)) =
      ∫⁻ p in diamond,
        angularAverage F (p.1,‖p.2‖) := by

  let G : AngularInput → ℝ≥0∞ :=
    fun p => angularAverage F p.1

  have hG : Measurable G :=
    (angularAverage_measurable F hF).comp
      measurable_fst

  have hslice :
      ∀ t : ℝ,
        (∫⁻ v in unitSpatialBall,
          angularSlice F t
            (‖v‖,⟪e,v⟫_ℝ/‖v‖)) =
        ∫⁻ v in unitSpatialBall,
          angularSlice G t
            (‖v‖,⟪e,v⟫_ℝ/‖v‖) := by

    intro t

    calc
      _ = ENNReal.ofReal Real.pi *
          ∫⁻ r in Ioo (0 : ℝ) 1,
            ENNReal.ofReal (2*r^2) *
              ∫⁻ c in Ioo (-1 : ℝ) 1,
                angularSlice F t (r,c) :=
        physical_direction_angular_integral
          e he (angularSlice F t)
          (angularSlice_measurable F hF t)

      _ = ENNReal.ofReal Real.pi *
          ∫⁻ r in Ioo (0 : ℝ) 1,
            ENNReal.ofReal (2*r^2) *
              ∫⁻ c in Ioo (-1 : ℝ) 1,
                angularSlice G t (r,c) := by

        congr 1

        apply lintegral_congr
        intro r

        have hh :
            (∫⁻ c in Ioo (-1 : ℝ) 1,
              angularSlice F t (r,c)) =
              ∫⁻ c in Ioo (-1 : ℝ) 1,
                angularSlice G t (r,c) :=
          angularSlice_average F t r

        rw [hh]

      _ = _ :=
        (physical_direction_angular_integral
          e he (angularSlice G t)
          (angularSlice_measurable G hG t)).symm

  calc
    _ = ∫⁻ t : ℝ,
        ∫⁻ v in unitSpatialBall,
          angularSlice F t
            (‖v‖,⟪e,v⟫_ℝ/‖v‖) :=
      diamond_angular_slices e F hF

    _ = ∫⁻ t : ℝ,
        ∫⁻ v in unitSpatialBall,
          angularSlice G t
            (‖v‖,⟪e,v⟫_ℝ/‖v‖) :=
      lintegral_congr hslice

    _ = _ :=
      (diamond_angular_slices e G hG).symm

theorem physical_angular_average
    (e : Space)
    (he : ‖e‖ = 1)
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p,
      F ((p.1,‖p.2‖),
        ⟪e,p.2⟫_ℝ/‖p.2‖)
      ∂uniform) =
      ∫⁻ p,
        angularAverage F (p.1,‖p.2‖)
        ∂uniform := by

  unfold uniform

  rw [lintegral_smul_measure,
    lintegral_smul_measure,
    smul_eq_mul,smul_eq_mul,
    physical_angular_average_raw e he F hF]

theorem physical_angular_rapidity_integral
    (e : Space)
    (he : ‖e‖ = 1)
    (F : AngularInput → ℝ≥0∞)
    (hF : Measurable F) :
    (∫⁻ p,
      F ((p.1,‖p.2‖),
        ⟪e,p.2⟫_ℝ/‖p.2‖)
        ∂uniform) =
      ENNReal.ofReal (16 : ℝ) *
        (∫⁻ q in rapidityRegion,
          ENNReal.ofReal
            (2*Real.exp (-2*q.1)) *
            (Chronos.RadialMeasure.density
              (Chronos.NullCoordinates.nullInverse
                (rapidityNull q)).2 *
              angularAverage F
                (Chronos.NullCoordinates.nullInverse
                  (rapidityNull q)))) := by

  rw [physical_angular_average e he F hF]

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
      hdim
      (angularAverage F)
      (angularAverage_measurable F hF)

  rw [← hd,
    ← Measure.volume_eq_prod,
    Chronos.GeometricTransport.normalized,
    Measure.restrict_apply_univ] at h

  exact h

#print axioms angularAverage_measurable
#print axioms physical_angular_average_raw
#print axioms physical_angular_average
#print axioms physical_angular_rapidity_integral

end

end Chronos.FourEvent
