import Mathlib

namespace Chronos.Frontier

noncomputable section

structure SchwarzschildIngoingEFMetric where
  mass : ℝ
  mass_pos : 0 < mass

structure SchwarzschildIngoingEFCoefficients where
  gvv : ℝ
  gvr : ℝ
  grv : ℝ
  grr : ℝ
  gθθ : ℝ
  gφφ : ℝ

def schwarzschildEFFactor
    (metric : SchwarzschildIngoingEFMetric)
    (r : ℝ) : ℝ :=
  1 - 2 * metric.mass / r

def schwarzschildIngoingEFCoefficients
    (metric : SchwarzschildIngoingEFMetric)
    (r θ : ℝ) :
    SchwarzschildIngoingEFCoefficients where
  gvv := -schwarzschildEFFactor metric r
  gvr := 1
  grv := 1
  grr := 0
  gθθ := r ^ 2
  gφφ := r ^ 2 * Real.sin θ ^ 2

def schwarzschildHorizonRadius
    (metric : SchwarzschildIngoingEFMetric) : ℝ :=
  2 * metric.mass

def schwarzschildOutgoingNullExpansion
    (metric : SchwarzschildIngoingEFMetric)
    (r : ℝ) : ℝ :=
  schwarzschildEFFactor metric r / r

theorem schwarzschildIngoingEF_cross_symmetric
    (metric : SchwarzschildIngoingEFMetric)
    (r θ : ℝ) :
    (schwarzschildIngoingEFCoefficients metric r θ).gvr =
      (schwarzschildIngoingEFCoefficients metric r θ).grv := by
  rfl

theorem schwarzschildHorizonRadius_pos
    (metric : SchwarzschildIngoingEFMetric) :
    0 < schwarzschildHorizonRadius metric := by
  unfold schwarzschildHorizonRadius
  nlinarith [metric.mass_pos]

theorem schwarzschildOutgoingNullExpansion_eq_zero_iff
    (metric : SchwarzschildIngoingEFMetric)
    {r : ℝ}
    (hr : 0 < r) :
    schwarzschildOutgoingNullExpansion metric r = 0 ↔
      r = schwarzschildHorizonRadius metric := by
  have hr0 : r ≠ 0 := ne_of_gt hr
  constructor
  · intro h
    unfold schwarzschildOutgoingNullExpansion
      schwarzschildEFFactor at h
    field_simp [hr0] at h
    unfold schwarzschildHorizonRadius
    linarith
  · intro h
    rw [h]
    unfold schwarzschildOutgoingNullExpansion
      schwarzschildEFFactor
      schwarzschildHorizonRadius
    have hM0 : metric.mass ≠ 0 :=
      ne_of_gt metric.mass_pos
    field_simp [hM0]
    ring

end

end Chronos.Frontier
