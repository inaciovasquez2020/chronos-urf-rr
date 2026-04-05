import Mathlib

namespace Chronos

universe v

def xorFold : List Bool → Bool
  | [] => false
  | b :: bs => if b then !(xorFold bs) else xorFold bs

def parityPair {E : Type v} (edges : List E) (h : E → Bool) : Bool :=
  xorFold (edges.map h)

end Chronos
