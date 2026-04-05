import Mathlib

namespace Chronos

universe u v

structure EFTranscript (V : Type u) where
  moves : List V

structure Cycle (E : Type v) where
  edges : List E

def xorFold : List Bool → Bool
  | [] => false
  | b :: bs => if b then !(xorFold bs) else xorFold bs

def parityPair {E : Type v} (C : Cycle E) (h : E → Bool) : Bool :=
  xorFold (C.edges.map h)

def parity_sep {V : Type u} {E : Type v}
    (_T : EFTranscript V)
    (C : Cycle E)
    (h1 h2 : E → Bool) : Prop :=
  parityPair C h1 ≠ parityPair C h2

end Chronos
