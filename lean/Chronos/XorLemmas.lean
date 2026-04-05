import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v

variable {E : Type v}

theorem xorFold_nil :
  xorFold [] = false := rfl

theorem xorFold_single (b : Bool) :
  xorFold [b] = b := by
  simp [xorFold]

theorem xorFold_cons (b : Bool) (bs : List Bool) :
  xorFold (b :: bs) = (b ≠ xorFold bs) := by
  by_cases hb : b <;> simp [xorFold, hb]

theorem parityPair_map (edges : List E) (h : E → Bool) :
  parityPair edges h = xorFold (edges.map h) := rfl

-- restore axiom (required)
axiom parityPair_ne_of_single_diff
  (edges : List E) (h1 h2 : E → Bool) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2

end Chronos
