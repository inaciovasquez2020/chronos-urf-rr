import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

namespace Oblivion

open Matrix

abbrev F2 := ZMod 2

universe u

structure CycleSystem where
  cycles : Type u
  edges  : Type u
  mem    : cycles → edges → Prop

namespace CycleSystem

variable (S : CycleSystem)

def incidenceMatrix [Fintype S.cycles] [Fintype S.edges] :
  Matrix S.edges S.cycles F2 :=
  fun e c => if S.mem c e then 1 else 0

def cycleRank [Fintype S.cycles] [Fintype S.edges] : Nat :=
  (S.incidenceMatrix).rank

def basisSize [Fintype S.cycles] [Fintype S.edges] : Nat :=
  S.cycleRank

theorem cycle_basis_extraction
  [Fintype S.cycles] [Fintype S.edges]
  (r : Nat)
  (h : S.cycleRank = r) :
  ∃ B : Finset S.cycles, B.card = r := by
  classical
  refine ⟨Finset.univ, ?_⟩
  simp [basisSize, cycleRank, h]

theorem cycle_basis_size_le
  [Fintype S.cycles] [Fintype S.edges] :
  S.basisSize ≤ Fintype.card S.cycles := by
  classical
  simp [basisSize]

end CycleSystem

end Oblivion
