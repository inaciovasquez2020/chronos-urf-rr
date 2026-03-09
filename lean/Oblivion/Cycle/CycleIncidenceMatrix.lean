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

structure FinGraph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

namespace FinGraph

variable (G : FinGraph)

def edgeSet := G.E

def vertexSet := G.V

end FinGraph

structure CycleFamily (G : FinGraph) where
  C : Type u
  edgeMem : C → G.E → Prop

namespace CycleFamily

variable {G : FinGraph} (F : CycleFamily G)

def incidenceMatrix [Fintype F.C] [Fintype G.E] : Matrix G.E F.C F2 :=
  fun e c => if F.edgeMem c e then 1 else 0

def cycleRank [Fintype F.C] [Fintype G.E] : Nat :=
  Module.finrank F2 (Matrix.colSpace (F.incidenceMatrix))

def cycleSpaceDim [Fintype F.C] [Fintype G.E] : Nat :=
  F.cycleRank

theorem rank_incidence_eq_finrank_colSpace
  [Fintype F.C] [Fintype G.E] :
  (F.incidenceMatrix).rank = F.cycleRank := by
  classical
  simp [cycleRank]

theorem cycleRank_eq_cycleSpaceDim
  [Fintype F.C] [Fintype G.E] :
  F.cycleRank = F.cycleSpaceDim := by
  rfl

theorem rank_incidence_eq_cycleSpaceDim
  [Fintype F.C] [Fintype G.E] :
  (F.incidenceMatrix).rank = F.cycleSpaceDim := by
  classical
  rw [rank_incidence_eq_finrank_colSpace, cycleRank_eq_cycleSpaceDim]

end CycleFamily

end Oblivion
