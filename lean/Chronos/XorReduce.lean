import Mathlib
import Chronos.ParityPair
import Chronos.XorTail

namespace Chronos

universe v

variable {E : Type v}

theorem parityPair_cons_eq_iff_tail
  (x : E) (xs : List E) (h1 h2 : E → Bool)
  (hx : h1 x = h2 x) :
  parityPair (x :: xs) h1 ≠ parityPair (x :: xs) h2 ↔
  parityPair xs h1 ≠ parityPair xs h2 := by
  by_cases h1x : h1 x <;> by_cases h2x : h2 x <;>
    simp [parityPair, xorFold, h1x, h2x] at hx ⊢

end Chronos
