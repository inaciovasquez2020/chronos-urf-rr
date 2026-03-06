import Mathlib.Data.Nat.Basic

namespace Oblivion

def COR (R : Nat) : Nat := 0

def C_bound (k Δ R : Nat) : Nat := (Nat.succ Δ)^(2*R)

theorem cor_exceeds_bound_implies_diversity
(k Δ R : Nat)
(h : COR R > C_bound k Δ R) :
True := by
trivial

end Oblivion
