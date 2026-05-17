import Chronos.Frontier.FiniteRegisteredHyperbolicRateThickAssembly

/-!
Lyapunov fiber-bound route.

This file isolates the next analytic input without assuming that the finite
registered hyperbolic assembly exposes its temporary external scaffold names as
repository-native projections.

Boundary: route only; no construction of the analytic bounds.
-/

namespace Chronos
namespace Frontier
namespace LyapunovFiberBoundRoute

structure NaturalHyperbolicBoundSystem where
  lyapunovExpansion : Nat → ℝ
  fiberLoss : Nat → ℝ
  entropyMass : Nat → ℝ

structure LyapunovFiberBoundData
    (D : NaturalHyperbolicBoundSystem)
    (L B : ℝ) : Prop where
  expansion_lower : ∀ n : Nat, L ≤ D.lyapunovExpansion n
  loss_upper : ∀ n : Nat, D.fiberLoss n ≤ B
  entropy_controls_loss :
    ∀ n : Nat, D.lyapunovExpansion n - D.fiberLoss n ≤ D.entropyMass n
  gap_pos : 0 < L - B

structure LyapunovFiberUniformFloor
    (D : NaturalHyperbolicBoundSystem)
    (epsilon : ℝ) : Prop where
  epsilon_pos : 0 < epsilon
  uniform_floor : ∀ n : Nat, epsilon ≤ D.entropyMass n

def NaturalHyperbolicBoundUniversalGap
    (D : NaturalHyperbolicBoundSystem) : Prop :=
  ∃ epsilon : ℝ, LyapunovFiberUniformFloor D epsilon

theorem LyapunovFiberUniformFloor_from_bounds
    (D : NaturalHyperbolicBoundSystem)
    (L B : ℝ)
    (h : LyapunovFiberBoundData D L B) :
    LyapunovFiberUniformFloor D (L - B) := by
  constructor
  · exact h.gap_pos
  · intro n
    have hL : L ≤ D.lyapunovExpansion n := h.expansion_lower n
    have hB : D.fiberLoss n ≤ B := h.loss_upper n
    have hSub : L - B ≤ D.lyapunovExpansion n - D.fiberLoss n :=
      sub_le_sub hL hB
    have hEnt : D.lyapunovExpansion n - D.fiberLoss n ≤ D.entropyMass n :=
      h.entropy_controls_loss n
    exact le_trans hSub hEnt

theorem entropyMass_uniform_floor_from_bounds
    (D : NaturalHyperbolicBoundSystem)
    (L B : ℝ)
    (h : LyapunovFiberBoundData D L B)
    (n : Nat) :
    L - B ≤ D.entropyMass n :=
  (LyapunovFiberUniformFloor_from_bounds D L B h).uniform_floor n

theorem NaturalHyperbolicBoundUniversalGap_from_lyapunov_bounds
    (D : NaturalHyperbolicBoundSystem)
    (L B : ℝ)
    (h : LyapunovFiberBoundData D L B) :
    NaturalHyperbolicBoundUniversalGap D := by
  exact ⟨L - B, LyapunovFiberUniformFloor_from_bounds D L B h⟩

end LyapunovFiberBoundRoute
end Frontier
end Chronos
