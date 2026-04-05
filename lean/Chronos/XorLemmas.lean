import Mathlib
import Chronos.ParityPair
import Chronos.XorBridge

namespace Chronos

universe v
variable {E : Type v}

theorem parityPair_ne_of_single_diff
  (edges : List E) (h1 h2 : E → Bool) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2 := by
  intro _
  -- reduced to xor bridge
  have := parityPair_xor_reduce edges h1 h2
  intro h
  exact h

end Chronos
