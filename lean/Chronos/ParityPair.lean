import Mathlib

namespace Chronos

universe v

structure Cycle (E : Type v) where
  edges : List E

def xorFold : List Bool → Bool
  | [] => false
  | b :: bs => if b then !(xorFold bs) else xorFold bs

def parityPair {E : Type v} (C : Cycle E) (h : E → Bool) : Bool :=
  xorFold (C.edges.map h)

end Chronos
