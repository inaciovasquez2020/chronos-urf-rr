import Mathlib
import Chronos.ParityPair
import Chronos.XorCons

namespace Chronos

universe v

variable {E : Type v}

def supportSingleton (xs : List E) (d : E → Bool) : Prop :=
  ∃! e, e ∈ xs ∧ d e = true


end Chronos
