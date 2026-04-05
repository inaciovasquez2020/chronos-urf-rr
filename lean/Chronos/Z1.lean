import Mathlib

namespace Chronos

universe u v

structure Cycle (E : Type v) where
  edges : List E

def Z1 {V : Type u} {E : Type v}
    (boundary : Cycle E → Int)
    (support : Cycle E → Set V)
    (S : Set V)
    (C : Cycle E) : Prop :=
  boundary C = 0 ∧ support C ⊆ S

end Chronos
