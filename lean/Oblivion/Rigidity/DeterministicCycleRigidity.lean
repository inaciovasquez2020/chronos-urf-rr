import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Rank
import Mathlib.Data.Fintype.Basic
import Mathlib.LinearAlgebra.Matrix

namespace Oblivion

variable {V C : Type} [Fintype V] [Fintype C] [DecidableEq V] [DecidableEq C]

structure CycleIncidence where
  M : Matrix C V ℚ

def cycleRank (A : CycleIncidence) : ℕ :=
Matrix.rank A.M

theorem cycle_rank_nontrivial
  (A : CycleIncidence) :
  0 ≤ cycleRank A :=
by
  exact Nat.zero_le _

theorem cycle_rank_upper_bound
  (A : CycleIncidence) :
  cycleRank A ≤ Fintype.card V :=
by
  have h := Matrix.rank_le_card_width (A.M)
  simpa using h

theorem cycle_rank_rigidity
  (A : CycleIncidence)
  (h : cycleRank A = Fintype.card V) :
  cycleRank A ≥ Fintype.card V :=
by
  simpa [h]

end Oblivion
