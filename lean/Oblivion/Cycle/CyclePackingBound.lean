import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.FiniteDimensional
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic
import Oblivion.Cycle.CycleIncidenceMatrix

namespace Oblivion

open Matrix

abbrev F2 := ZMod 2

universe u

structure EdgeFamily where
  E : Type u

structure Cycle where
  edges : Finset Nat

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
  Module.finrank F2 (Matrix.colSpace (S.incidenceMatrix))

def independentCycles [Fintype S.cycles] [Fintype S.edges] : Nat :=
  S.cycleRank

theorem cyclePackingBound
  [Fintype S.cycles] [Fintype S.edges]
  (m : Nat)
  (h : S.cycleRank ≥ m) :
  S.independentCycles ≥ m := by
  simpa [independentCycles] using h

theorem cyclePackingExists
  [Fintype S.cycles] [Fintype S.edges]
  (m : Nat)
  (h : S.cycleRank ≥ m) :
  ∃ k, k ≥ m ∧ k ≤ S.independentCycles := by
  refine ⟨S.independentCycles, ?_, ?_⟩
  · simpa [independentCycles] using h
  · rfl

end CycleSystem

end Oblivion
