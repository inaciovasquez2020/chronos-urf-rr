import Oblivion.CycleOverlapRank
import Oblivion.CycleOverlapProperties

namespace Oblivion

variable {V : Type}

/-- Transport signatures differ somewhere if cycle overlap rank is large (skeleton). -/
theorem transport_signature_diversity
  (G : Graph V)
  (R T : Nat)
  (h : largeCycleOverlap G R T) :
  ∃ u v : V, signature G R u ≠ signature G R v := by
  admit

end Oblivion
