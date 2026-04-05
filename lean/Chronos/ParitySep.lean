import Mathlib
import Chronos.Transcript
import Chronos.ParityPair

namespace Chronos

universe u v

def parity_sep {V : Type u} {E : Type v}
    (_T : EFTranscript V)
    (edges : List E)
    (h1 h2 : E → Bool) : Prop :=
  parityPair edges h1 ≠ parityPair edges h2

end Chronos
