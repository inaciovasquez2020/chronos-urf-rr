import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v

variable {E : Type v}

def diffFun (h1 h2 : E → Bool) : E → Bool :=
  fun e => Bool.xor (h1 e) (h2 e)

theorem parityPair_diff_rewrite
  (edges : List E) (h1 h2 : E → Bool) :
  parityPair edges h1 ≠ parityPair edges h2 →
  xorFold (edges.map (diffFun h1 h2)) = true := by
  intro h
  cases edges with
  | nil =>
      simp [parityPair] at h
  | cons x xs =>
      simp [parityPair, xorFold, diffFun]

end Chronos
