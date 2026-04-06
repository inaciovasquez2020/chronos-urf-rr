import Mathlib
import Chronos.ParityPair
import Chronos.ParitySepProof

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

theorem parityPair_ne_of_single_diff
  (edges : List E) (h1 h2 : E → Bool)
  (h_nodup : edges.Nodup) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2 :=
by
  intro huniq
  exact parityPair_ne_of_single_diff' edges h1 h2 h_nodup huniq

end Chronos
