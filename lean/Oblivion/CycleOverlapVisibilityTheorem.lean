import Oblivion.WL2FO3BridgeFinal
import Oblivion.CycleOverlapRank

namespace Oblivion

variable {V : Type}

/-- Final Cycle-Overlap Visibility Theorem (skeleton).

Large cycle-overlap rank forces FO³ type diversity.
-/
theorem cycle_overlap_visibility
  (G : Graph V)
  (R T : Nat)
  (h : largeCycleOverlap G R T) :
  ∃ u v : V, fo3Type G u ≠ fo3Type G v := by
  exact corR_implies_fo3 (G:=G) (R:=R) (T:=T) h

end Oblivion
