import Mathlib

namespace Chronos

universe u v

structure EFTranscript (V : Type u) :=
  (moves : List V)

def buildTranscript {V : Type u} {R : Nat}
  (h1 h2 : V → Bool) : EFTranscript V :=
  { moves := [] }

end Chronos
