import Mathlib
import Chronos.ParityPair
import Chronos.XorCons

namespace Chronos

universe v
variable {E : Type v}

def diffFun (h1 h2 : E → Bool) : E → Bool :=
  fun e => Bool.xor (h1 e) (h2 e)

theorem parityPair_xor_reduce
  (edges : List E) (h1 h2 : E → Bool) :
  parityPair edges h1 ≠ parityPair edges h2 →
  xorFold (edges.map (diffFun h1 h2)) = true := by
  intro h
  induction edges with
  | nil =>
      simp [parityPair] at h
  | cons x xs ih =>
      simp [parityPair, xorFold, diffFun] at h ⊢
      by_cases hx : h1 x = h2 x
      · exact ih h
      · simp [hx]

end Chronos
