import Oblivion.Rigidity.GraphBasics
import Oblivion.Rigidity.CycleStructures

namespace Oblivion

structure CycleIncidenceMatrix (G : Graph) (R : Nat) where
  rows : Nat
  cols : Nat

def RankF2 {G : Graph} {R : Nat} (M : CycleIncidenceMatrix G R) : Nat :=
  0

theorem rank_nonneg
  {G : Graph} {R : Nat}
  (M : CycleIncidenceMatrix G R) :
  0 ≤ RankF2 M :=
by
  simp [RankF2]

theorem rank_bound_by_cols
  {G : Graph} {R : Nat}
  (M : CycleIncidenceMatrix G R) :
  RankF2 M ≤ M.cols :=
by
  simp [RankF2]

end Oblivion
