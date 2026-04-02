namespace Chronos

def ED (n : Nat) : Nat := n

def Hbits (n : Nat) : ℝ := (n : ℝ)

theorem normalization_lower_bound_concrete
  (n : Nat)
  (λ : ℝ)
  (hλ : λ > 0) :
  λ * (ED n : ℝ) ≥ Hbits n := by
  have : λ * (n : ℝ) ≥ (n : ℝ) := by
    have := mul_le_mul_of_nonneg_right (le_of_lt hλ) (by exact_mod_cast Nat.zero_le n)
    simpa using this
  simpa [ED, Hbits]

end Chronos
