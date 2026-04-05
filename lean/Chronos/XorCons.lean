import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v

variable {E : Type v}

theorem xorFold_cons_cases
  (x : Bool) (xs : List Bool) :
  xorFold (x :: xs) = (x ≠ xorFold xs) := by
  by_cases hx : x <;> simp [xorFold, hx]

end Chronos
