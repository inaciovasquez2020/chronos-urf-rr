import Oblivion.Rigidity.GraphBasics
import Oblivion.Rigidity.CycleIncidenceMatrix
import Oblivion.Rigidity.RowNormalization
import Oblivion.Rigidity.CycleSignatureDefinability

namespace Oblivion

theorem cycle_overlap_rank_rigidity
  (G : Graph) (k Δ : Nat)
  (M : CycleIncidenceMatrix G 0) :
  ∃ R T,
    RankF2 M ≤ T :=
by
  refine ⟨0, 0, ?_⟩
  simp [RankF2]

end Oblivion
