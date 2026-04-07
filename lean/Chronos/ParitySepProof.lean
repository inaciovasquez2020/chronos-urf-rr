import Mathlib
import Chronos.ParityPair
import Chronos.ParitySep
import Chronos.XorLemmas

namespace Chronos

universe v
variable {E : Type v} [DecidableEq E]

def diffEdge (edges : List E) (h1 h2 : E → Bool) : Prop :=
  ∃ e, e ∈ edges ∧ h1 e ≠ h2 e

theorem parityPair_ne_of_single_diff'
  (edges : List E) (h1 h2 : E → Bool)
  (h_nodup : edges.Nodup) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2 :=
  parityPair_ne_of_single_diff edges h1 h2 h_nodup

end Chronos
