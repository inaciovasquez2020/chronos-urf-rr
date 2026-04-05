import Mathlib

namespace Chronos

universe u v

structure EFTranscript (V : Type u) where
  moves : List V

structure Cycle (E : Type v) where
  edges : List E

def close_seeded {V : Type u} {E : Type v}
  (_T : EFTranscript V) : Cycle E :=
  { edges := [] }

end Chronos
