namespace Oblivion

theorem packing_bound
(n Δ R : Nat) :
n ≤ (Nat.succ Δ)^(R+1) * n := by
  have h : (1 : Nat) ≤ (Nat.succ Δ)^(R+1) := by
    exact Nat.one_le_pow _ _
  exact Nat.mul_le_mul_right _ h

end Oblivion
