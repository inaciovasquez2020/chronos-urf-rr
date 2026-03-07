import Oblivion.WL2FO3Bridge

namespace Oblivion

variable {V : Type}

/-- Final statement of the Cycle-Overlap Visibility theorem skeleton. -/
theorem cycle_overlap_visibility
  (G : Graph V)
  (h : COR_R ≥ T) :
  ∃ u v : V, fo3Type G u ≠ fo3Type G v := by
  exact corR_implies_fo3_diversity (G:=G) h

end Oblivion
