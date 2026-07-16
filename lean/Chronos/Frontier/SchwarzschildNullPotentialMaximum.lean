import Chronos.Frontier.SchwarzschildIngoingEFHorizon

namespace Chronos.Frontier

noncomputable section

def schwarzschildNullEffectivePotential
    (metric : SchwarzschildIngoingEFMetric)
    (r : ℝ) : ℝ :=
  schwarzschildEFFactor metric r / r ^ 2

def schwarzschildPhotonSphereRadius
    (metric : SchwarzschildIngoingEFMetric) : ℝ :=
  3 * metric.mass

theorem schwarzschildPhotonSphereRadius_exterior
    (metric : SchwarzschildIngoingEFMetric) :
    schwarzschildHorizonRadius metric <
      schwarzschildPhotonSphereRadius metric := by
  unfold schwarzschildHorizonRadius
    schwarzschildPhotonSphereRadius
  nlinarith [metric.mass_pos]

theorem schwarzschildNullEffectivePotential_gap_identity
    (metric : SchwarzschildIngoingEFMetric)
    (r : ℝ)
    (hr : r ≠ 0) :
    schwarzschildNullEffectivePotential
          metric
          (schwarzschildPhotonSphereRadius metric) -
        schwarzschildNullEffectivePotential metric r =
      ((r - schwarzschildPhotonSphereRadius metric) ^ 2 *
          (r + 6 * metric.mass)) /
        (27 * metric.mass ^ 2 * r ^ 3) := by
  have hM0 : metric.mass ≠ 0 :=
    ne_of_gt metric.mass_pos
  unfold schwarzschildNullEffectivePotential
    schwarzschildPhotonSphereRadius
    schwarzschildEFFactor
  field_simp [hM0, hr] ; ring

theorem schwarzschildNullEffectivePotential_le_photonSphere
    (metric : SchwarzschildIngoingEFMetric)
    {r : ℝ}
    (hrExterior :
      schwarzschildHorizonRadius metric < r) :
    schwarzschildNullEffectivePotential metric r ≤
      schwarzschildNullEffectivePotential
        metric
        (schwarzschildPhotonSphereRadius metric) := by
  have hrPos : 0 < r := by
    have hHorizonPos :=
      schwarzschildHorizonRadius_pos metric
    nlinarith

  have hTailPos :
      0 < r + 6 * metric.mass := by
    nlinarith [metric.mass_pos]

  have hDenPos :
      0 < 27 * metric.mass ^ 2 * r ^ 3 := by
    exact
      mul_pos
        (mul_pos
          (by norm_num)
          (pow_pos metric.mass_pos 2))
        (pow_pos hrPos 3)

  have hNumeratorNonneg :
      0 ≤
        (r - schwarzschildPhotonSphereRadius metric) ^ 2 *
          (r + 6 * metric.mass) :=
    mul_nonneg
      (sq_nonneg
        (r - schwarzschildPhotonSphereRadius metric))
      hTailPos.le

  have hFractionNonneg :
      0 ≤
        ((r - schwarzschildPhotonSphereRadius metric) ^ 2 *
            (r + 6 * metric.mass)) /
          (27 * metric.mass ^ 2 * r ^ 3) :=
    div_nonneg hNumeratorNonneg hDenPos.le

  have hGap :=
    schwarzschildNullEffectivePotential_gap_identity
      metric r (ne_of_gt hrPos)

  nlinarith

theorem schwarzschildNullEffectivePotential_lt_photonSphere_of_ne
    (metric : SchwarzschildIngoingEFMetric)
    {r : ℝ}
    (hrExterior :
      schwarzschildHorizonRadius metric < r)
    (hrNe :
      r ≠ schwarzschildPhotonSphereRadius metric) :
    schwarzschildNullEffectivePotential metric r <
      schwarzschildNullEffectivePotential
        metric
        (schwarzschildPhotonSphereRadius metric) := by
  have hrPos : 0 < r := by
    have hHorizonPos :=
      schwarzschildHorizonRadius_pos metric
    nlinarith

  have hTailPos :
      0 < r + 6 * metric.mass := by
    nlinarith [metric.mass_pos]

  have hDifferenceNe :
      r - schwarzschildPhotonSphereRadius metric ≠ 0 :=
    sub_ne_zero.mpr hrNe

  have hSquarePos :
      0 <
        (r - schwarzschildPhotonSphereRadius metric) ^ 2 := by
    exact sq_pos_of_ne_zero hDifferenceNe

  have hDenPos :
      0 < 27 * metric.mass ^ 2 * r ^ 3 := by
    exact
      mul_pos
        (mul_pos
          (by norm_num)
          (pow_pos metric.mass_pos 2))
        (pow_pos hrPos 3)

  have hFractionPos :
      0 <
        ((r - schwarzschildPhotonSphereRadius metric) ^ 2 *
            (r + 6 * metric.mass)) /
          (27 * metric.mass ^ 2 * r ^ 3) :=
    div_pos
      (mul_pos hSquarePos hTailPos)
      hDenPos

  have hGap :=
    schwarzschildNullEffectivePotential_gap_identity
      metric r (ne_of_gt hrPos)

  nlinarith

theorem schwarzschildNullEffectivePotential_eq_max_iff
    (metric : SchwarzschildIngoingEFMetric)
    {r : ℝ}
    (hrExterior :
      schwarzschildHorizonRadius metric < r) :
    schwarzschildNullEffectivePotential metric r =
        schwarzschildNullEffectivePotential
          metric
          (schwarzschildPhotonSphereRadius metric) ↔
      r = schwarzschildPhotonSphereRadius metric := by
  constructor
  · intro hEqual
    by_contra hrNe
    have hStrict :=
      schwarzschildNullEffectivePotential_lt_photonSphere_of_ne
        metric hrExterior hrNe
    linarith
  · intro hr
    rw [hr]

theorem schwarzschildNullEffectivePotential_unique_exterior_maximum
    (metric : SchwarzschildIngoingEFMetric)
    {r : ℝ}
    (hrExterior :
      schwarzschildHorizonRadius metric < r) :
    (∀ s,
        schwarzschildHorizonRadius metric < s →
          schwarzschildNullEffectivePotential metric s ≤
            schwarzschildNullEffectivePotential metric r) ↔
      r = schwarzschildPhotonSphereRadius metric := by
  constructor
  · intro hMaximum

    have hPhotonExterior :
        schwarzschildHorizonRadius metric <
          schwarzschildPhotonSphereRadius metric :=
      schwarzschildPhotonSphereRadius_exterior metric

    have hPhotonLe :
        schwarzschildNullEffectivePotential
            metric
            (schwarzschildPhotonSphereRadius metric) ≤
          schwarzschildNullEffectivePotential metric r :=
      hMaximum
        (schwarzschildPhotonSphereRadius metric)
        hPhotonExterior

    have hRLe :
        schwarzschildNullEffectivePotential metric r ≤
          schwarzschildNullEffectivePotential
            metric
            (schwarzschildPhotonSphereRadius metric) :=
      schwarzschildNullEffectivePotential_le_photonSphere
        metric hrExterior

    have hEqual :
        schwarzschildNullEffectivePotential metric r =
          schwarzschildNullEffectivePotential
            metric
            (schwarzschildPhotonSphereRadius metric) :=
      le_antisymm hRLe hPhotonLe

    exact
      (schwarzschildNullEffectivePotential_eq_max_iff
        metric hrExterior).mp hEqual

  · intro hr
    subst r
    intro s hsExterior
    exact
      schwarzschildNullEffectivePotential_le_photonSphere
        metric hsExterior

end

end Chronos.Frontier
