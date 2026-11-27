import NullRapidityMeasure

open MeasureTheory Set
open scoped ENNReal

namespace Chronos.FourEvent

open Chronos.PhysicalMoments
open Chronos.NullCoordinates
open Chronos.RadialMeasure

noncomputable section

private theorem nullInverse_measurable :
    Measurable nullInverse := by
  unfold nullInverse
  fun_prop

private theorem density_measurable :
    Measurable density := by
  unfold density
  apply Measurable.ennreal_ofReal
  fun_prop

theorem radialLaw_rapidity_integral
    (g : Plane → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p in region,g p
      ∂((volume : Measure ℝ).prod radialLaw)) =
      ENNReal.ofReal (1/2 : ℝ) *
        (∫⁻ q in rapidityRegion,
          ENNReal.ofReal
            (2*Real.exp (-2*q.1)) *
            (density
              (nullInverse (rapidityNull q)).2 *
              g (nullInverse (rapidityNull q)))) := by

  let K : Plane → ℝ≥0∞ :=
    fun z =>
      density (nullInverse z).2 *
        g (nullInverse z)

  have hK : Measurable K := by
    unfold K
    exact
      (density_measurable.comp
        (measurable_snd.comp
          nullInverse_measurable)).mul
        (hg.comp nullInverse_measurable)

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

  have hweighted :
      (∫⁻ p in region,g p
        ∂((volume : Measure ℝ).prod radialLaw)) =
      ∫⁻ p in sourceRegion,
        density p.2 * g p := by

    rw [radialLaw,
      prod_withDensity_right density_measurable,
      hp,
      restrict_withDensity
        region_open.measurableSet,
      Measure.restrict_restrict
        region_open.measurableSet]

    exact lintegral_withDensity_eq_lintegral_mul
      _
      (show Measurable
        (fun z : Plane => density z.2)
        from density_measurable.comp measurable_snd)
      hg

  calc
    _ = ∫⁻ p in sourceRegion,
        density p.2 * g p :=
      hweighted

    _ = ∫⁻ p in sourceRegion,
        K (nullMap p) := by

      apply lintegral_congr
      intro p
      dsimp only [K]
      rw [null_left_inverse]

    _ = ENNReal.ofReal (1/2 : ℝ) *
        (∫⁻ z in triangle,K z) :=
      null_change_of_variables K hK

    _ = _ := by
      rw [null_rapidity_integral K hK]

section Physical

variable {E : Type*}
variable [NormedAddCommGroup E]
variable [NormedSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E] [BorelSpace E]

theorem normalized_physical_rapidity_integral
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (g : Plane → ℝ≥0∞)
    (hg : Measurable g) :
    (∫⁻ p : ℝ × E,
      g (radialMap p)
      ∂Chronos.GeometricTransport.normalized
        (((volume : Measure ℝ).prod μ).restrict
          (Chronos.MinkowskiDiamond.diamond
            (0 : ℝ × E)
            Chronos.MinkowskiDiamond.tip))) =
      ENNReal.ofReal (16 : ℝ) *
        (∫⁻ q in rapidityRegion,
          ENNReal.ofReal
            (2*Real.exp (-2*q.1)) *
            (density
              (nullInverse (rapidityNull q)).2 *
              g (nullInverse (rapidityNull q)))) := by

  let C := μ (Metric.closedBall (0:E) 1)

  let A : ℝ≥0∞ :=
    C * ENNReal.ofReal (1/32 : ℝ)

  let I : ℝ≥0∞ :=
    ∫⁻ p in region,g p
      ∂((volume : Measure ℝ).prod radialLaw)

  have hC0 : C ≠ 0 :=
    (Metric.measure_closedBall_pos μ
      (0:E) zero_lt_one).ne'

  have hCT : C ≠ ∞ :=
    (isCompact_closedBall
      (0:E) 1).measure_lt_top.ne

  have hA0 : A ≠ 0 := by
    dsimp only [A]
    exact mul_ne_zero hC0
      (by norm_num)

  have hAT : A ≠ ∞ := by
    dsimp only [A]
    exact ENNReal.mul_ne_top hCT
      ENNReal.ofReal_ne_top

  have hCmul :
      A * ENNReal.ofReal (32 : ℝ) = C := by

    unfold A

    rw [mul_assoc,
      ← ENNReal.ofReal_mul
        (by norm_num : (0:ℝ) ≤ 1/32)]

    norm_num

  unfold Chronos.GeometricTransport.normalized

  rw [lintegral_smul_measure,
    smul_eq_mul,
    Measure.restrict_apply_univ,
    Chronos.NormalizedMoments.physical_diamond_mass
      μ hdim,
    physical_radial_integral μ hdim g hg]

  change A⁻¹ * (C * I) = _

  calc
    _ = A⁻¹ *
        (A * (ENNReal.ofReal (32 : ℝ) * I)) := by

      rw [← hCmul] <;> ac_rfl

    _ = ENNReal.ofReal (32 : ℝ) * I :=
      ENNReal.inv_mul_cancel_left hA0 hAT

    _ = _ := by
      unfold I
      rw [radialLaw_rapidity_integral g hg,
        ← mul_assoc,
        ← ENNReal.ofReal_mul
          (by norm_num : (0:ℝ) ≤ 32)]
      norm_num

end Physical

#print axioms radialLaw_rapidity_integral
#print axioms normalized_physical_rapidity_integral

end

end Chronos.FourEvent
