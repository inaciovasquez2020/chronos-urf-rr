import Mathlib
import Chronos.ParityPair
import Chronos.ParitySep

namespace Chronos

universe u v

def diffEdge {E : Type v} (edges : List E) (h1 h2 : E → Bool) : Prop :=
  ∃ e, e ∈ edges ∧ h1 e ≠ h2 e

axiom parityPair_ne_of_single_diff
  {E : Type v}
  (edges : List E) (h1 h2 : E → Bool) :
  (∃ e, e ∈ edges ∧ h1 e ≠ h2 e) →
  (∀ e, e ∈ edges → h1 e = h2 e ∨ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2

end Chronos
