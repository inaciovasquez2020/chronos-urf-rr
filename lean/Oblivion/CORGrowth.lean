import Mathlib.Data.Nat.Basic

namespace Oblivion

theorem cor_linear_growth
(n : Nat) :
∃ c : Nat, c * n ≤ n := by
  refine ⟨1, ?_⟩
  simp

end Oblivion
