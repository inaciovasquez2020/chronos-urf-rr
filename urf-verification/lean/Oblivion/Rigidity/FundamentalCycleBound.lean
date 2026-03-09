import Mathlib.Tactic
import Mathlib.Data.Nat.Basic

namespace Cyclone.CCL.Fundamental

/-- Abstract fundamental cycle record. -/
structure FundamentalCycle where
  path₁ : List Nat
  path₂ : List Nat

/-- Cycle length definition. -/
def cycleLength (C : FundamentalCycle) : ℕ :=
  C.path₁.length + C.path₂.length + 1

/-- Fundamental cycle locality bound. -/
theorem fundamental_cycle_length_bound
    (C : FundamentalCycle)
    (R : ℕ)
    (h₁ : C.path₁.length ≤ R)
    (h₂ : C.path₂.length ≤ R) :
    cycleLength C ≤ 2 * R + 1 := by
  unfold cycleLength
  have hsum : C.path₁.length + C.path₂.length ≤ 2 * R := by
    exact Nat.add_le_add h₁ h₂
  have := Nat.succ_le_succ hsum
  simpa [two_mul] using this

end Cyclone.CCL.Fundamental
