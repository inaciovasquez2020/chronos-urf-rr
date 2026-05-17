import Chronos.Frontier.LyapunovFiberBoundDataCertificate

/-!
Unrestricted Lyapunov certificate obstruction.

This file proves that the unrestricted analytic construction

  ∀ D, ∃ L B, LyapunovFiberBoundData D L B

is false for the current repository-native `NaturalHyperbolicBoundSystem`
interface.

Boundary: obstruction only; no replacement restricted domain is constructed here.
-/

namespace Chronos
namespace Frontier
namespace LyapunovCertificateUnrestrictedObstruction

open LyapunovFiberBoundRoute

def zeroBoundSystem : NaturalHyperbolicBoundSystem where
  lyapunovExpansion := fun _ => 0
  fiberLoss := fun _ => 0
  entropyMass := fun _ => 0

theorem no_LyapunovFiberBoundData_zeroBoundSystem
    (L B : ℝ) :
    ¬ LyapunovFiberBoundData zeroBoundSystem L B := by
  intro h
  have hL : L ≤ 0 := h.expansion_lower 0
  have hB : 0 ≤ B := h.loss_upper 0
  have hGapNonpos : L - B ≤ 0 := by
    exact sub_nonpos.mpr (le_trans hL hB)
  exact not_lt_of_ge hGapNonpos h.gap_pos

theorem unrestricted_LyapunovFiberBoundData_false :
    ¬ ∀ D : NaturalHyperbolicBoundSystem,
      ∃ L B : ℝ, LyapunovFiberBoundData D L B := by
  intro h
  rcases h zeroBoundSystem with ⟨L, B, hLB⟩
  exact no_LyapunovFiberBoundData_zeroBoundSystem L B hLB

theorem unrestricted_LyapunovFiberBoundCertificate_false :
    ¬ ∀ D : NaturalHyperbolicBoundSystem,
      ∃ _ : LyapunovFiberBoundDataCertificate.LyapunovFiberBoundCertificate D, True := by
  intro h
  rcases h zeroBoundSystem with ⟨c, hc⟩
  exact no_LyapunovFiberBoundData_zeroBoundSystem c.L c.B
    (by exact LyapunovFiberBoundDataCertificate.LyapunovFiberBoundData_from_certificate zeroBoundSystem c)

end LyapunovCertificateUnrestrictedObstruction
end Frontier
end Chronos
