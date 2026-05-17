import Chronos.Frontier.LyapunovFiberBoundRoute

/-!
Lyapunov fiber-bound data certificate.

This closes the repository-native construction interface for

  LyapunovFiberBoundData D L B

from an explicit certificate carrying the lower expansion bound, upper loss
bound, entropy-control inequality, and positive gap.

Boundary: certificate construction only; no analytic construction of the
certificate for an unrestricted external system.
-/

namespace Chronos
namespace Frontier
namespace LyapunovFiberBoundDataCertificate

open LyapunovFiberBoundRoute

structure LyapunovFiberBoundCertificate
    (D : NaturalHyperbolicBoundSystem) where
  L : ℝ
  B : ℝ
  expansion_lower : ∀ n : Nat, L ≤ D.lyapunovExpansion n
  loss_upper : ∀ n : Nat, D.fiberLoss n ≤ B
  entropy_controls_loss :
    ∀ n : Nat, D.lyapunovExpansion n - D.fiberLoss n ≤ D.entropyMass n
  gap_pos : 0 < L - B

theorem LyapunovFiberBoundData_from_certificate
    (D : NaturalHyperbolicBoundSystem)
    (c : LyapunovFiberBoundCertificate D) :
    LyapunovFiberBoundData D c.L c.B := by
  exact {
    expansion_lower := c.expansion_lower
    loss_upper := c.loss_upper
    entropy_controls_loss := c.entropy_controls_loss
    gap_pos := c.gap_pos
  }

theorem exists_LB_LyapunovFiberBoundData_from_certificate
    (D : NaturalHyperbolicBoundSystem)
    (c : LyapunovFiberBoundCertificate D) :
    ∃ L B : ℝ, LyapunovFiberBoundData D L B := by
  exact ⟨c.L, c.B, LyapunovFiberBoundData_from_certificate D c⟩

theorem LyapunovFiberUniformFloor_from_certificate
    (D : NaturalHyperbolicBoundSystem)
    (c : LyapunovFiberBoundCertificate D) :
    LyapunovFiberUniformFloor D (c.L - c.B) := by
  exact LyapunovFiberUniformFloor_from_bounds
    D c.L c.B
    (LyapunovFiberBoundData_from_certificate D c)

theorem NaturalHyperbolicBoundUniversalGap_from_certificate
    (D : NaturalHyperbolicBoundSystem)
    (c : LyapunovFiberBoundCertificate D) :
    NaturalHyperbolicBoundUniversalGap D := by
  exact NaturalHyperbolicBoundUniversalGap_from_lyapunov_bounds
    D c.L c.B
    (LyapunovFiberBoundData_from_certificate D c)

end LyapunovFiberBoundDataCertificate
end Frontier
end Chronos
