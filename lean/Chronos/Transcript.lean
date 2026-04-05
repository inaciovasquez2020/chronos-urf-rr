import Mathlib

namespace Chronos

universe u

structure EFTranscript (V : Type u) where
  moves : List V

def buildTranscript {V : Type u} {_R : Nat}
  (_h1 _h2 : V → Bool) : EFTranscript V :=
  { moves := [] }

end Chronos
