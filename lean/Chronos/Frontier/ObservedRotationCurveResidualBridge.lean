import Mathlib

namespace Chronos.Frontier

structure RotationCurveResidualPoint where
  G : ℚ
  radius : ℚ
  velocity : ℚ
  baryonicMass : ℚ
  hG : 0 < G
  hr : 0 ≤ radius
  hv : 0 ≤ velocity
  hb : 0 ≤ baryonicMass

def requiredMass (p : RotationCurveResidualPoint) : ℚ :=
  (p.velocity * p.velocity * p.radius) / p.G

def gdmResidual (p : RotationCurveResidualPoint) : ℚ :=
  max 0 (requiredMass p - p.baryonicMass)

theorem gdmResidual_nonnegative
    (p : RotationCurveResidualPoint) :
    0 ≤ gdmResidual p := by
  unfold gdmResidual
  exact le_max_left 0 (requiredMass p - p.baryonicMass)

theorem gdmResidual_eq_zero_of_required_le_baryonic
    (p : RotationCurveResidualPoint)
    (h : requiredMass p ≤ p.baryonicMass) :
    gdmResidual p = 0 := by
  unfold gdmResidual
  exact max_eq_left (sub_nonpos.mpr h)

theorem gdmResidual_eq_required_sub_baryonic_of_baryonic_lt_required
    (p : RotationCurveResidualPoint)
    (h : p.baryonicMass < requiredMass p) :
    gdmResidual p = requiredMass p - p.baryonicMass := by
  unfold gdmResidual
  exact max_eq_right (sub_nonneg.mpr (le_of_lt h))

theorem gdmResidual_eq_zero_iff_required_le_baryonic
    (p : RotationCurveResidualPoint) :
    gdmResidual p = 0 ↔ requiredMass p ≤ p.baryonicMass := by
  constructor
  · intro h
    unfold gdmResidual at h
    have hle :
        requiredMass p - p.baryonicMass ≤
          max 0 (requiredMass p - p.baryonicMass) :=
      le_max_right 0 (requiredMass p - p.baryonicMass)
    rw [h] at hle
    exact sub_nonpos.mp hle
  · intro h
    exact gdmResidual_eq_zero_of_required_le_baryonic p h

theorem gdmResidual_pos_iff_baryonic_lt_required
    (p : RotationCurveResidualPoint) :
    0 < gdmResidual p ↔ p.baryonicMass < requiredMass p := by
  constructor
  · intro h
    by_contra hb
    have hle : requiredMass p ≤ p.baryonicMass := le_of_not_gt hb
    have hz : gdmResidual p = 0 :=
      gdmResidual_eq_zero_of_required_le_baryonic p hle
    rw [hz] at h
    exact (lt_irrefl 0 h)
  · intro h
    rw [gdmResidual_eq_required_sub_baryonic_of_baryonic_lt_required p h]
    exact sub_pos.mpr h

theorem residual_zero_iff_baryonic_dominates
    (p : RotationCurveResidualPoint) :
    gdmResidual p = 0 ↔ p.baryonicMass ≥ requiredMass p := by
  exact gdmResidual_eq_zero_iff_required_le_baryonic p

theorem residual_positive_iff_baryonic_less_required
    (p : RotationCurveResidualPoint) :
    0 < gdmResidual p ↔ p.baryonicMass < requiredMass p := by
  exact gdmResidual_pos_iff_baryonic_lt_required p

end Chronos.Frontier
