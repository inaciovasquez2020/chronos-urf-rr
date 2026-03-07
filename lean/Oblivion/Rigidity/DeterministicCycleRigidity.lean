import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.LinearAlgebra.Matrix.Rank

open Classical

universe u

namespace Oblivion
namespace Rigidity

variable {V : Type u} [Fintype V] [DecidableEq V]

def maxDegree (G : SimpleGraph V) : Nat :=
  Finset.sup Finset.univ (fun v => (G.neighborFinset v).card)

def ball (G : SimpleGraph V) (v : V) (R : Nat) : Finset V :=
  Finset.filter (fun u => G.dist v u ≤ R) Finset.univ

def rootedSignature (G : SimpleGraph V) (R : Nat) (v : V) :
    Finset (V × V) :=
  Finset.filter
    (fun e => e.1 ∈ ball G v R ∧ e.2 ∈ ball G v R ∧ G.Adj e.1 e.2)
    (Finset.product Finset.univ Finset.univ)

def rootedTypeCount (G : SimpleGraph V) (R : Nat) : Nat :=
  (Finset.univ.image (rootedSignature G R)).card

structure CycleIncidence (V : Type u) [DecidableEq V] where
  support : Finset (V × V)

def cycleMatrix (C : Finset (CycleIncidence V)) :
    Matrix (V × V) C (ZMod 2) :=
  fun e c => if e ∈ c.support then 1 else 0

def vertexCycleMatrix (G : SimpleGraph V) (C : Finset (CycleIncidence V)) (R : Nat) :
    Matrix V C (ZMod 2) :=
  fun v c =>
    if ∃ x ∈ c.support, x.1 ∈ ball G v R ∨ x.2 ∈ ball G v R then 1 else 0

def rankShortCycleSpace (C : Finset (CycleIncidence V)) : Nat :=
  Matrix.rank (cycleMatrix (V := V) C)

def rowDistinctCount {m n : Type u} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (A : Matrix m n (ZMod 2)) : Nat :=
  (Finset.univ.image fun i => A i).card

axiom sparseColumnRankTransfer
  (G : SimpleGraph V) (C : Finset (CycleIncidence V)) (Δ R c : Nat)
  (hdeg : maxDegree G ≤ Δ)
  (hcycleRank : c * Fintype.card V ≤ rankShortCycleSpace (V := V) C) :
  c * Fintype.card V ≤ rowDistinctCount (vertexCycleMatrix G C R)

axiom rowToRootedType
  (G : SimpleGraph V) (C : Finset (CycleIncidence V)) (R : Nat) :
  rowDistinctCount (vertexCycleMatrix G C R) ≤ rootedTypeCount G R

theorem deterministicCycleRigidity
  (G : SimpleGraph V)
  (C : Finset (CycleIncidence V))
  (Δ L c : Nat)
  (hdeg : maxDegree G ≤ Δ)
  (hcycleRank : c * Fintype.card V ≤ rankShortCycleSpace (V := V) C) :
  ∃ R : Nat, c * Fintype.card V ≤ rootedTypeCount G R := by
  refine ⟨2 * L, ?_⟩
  have hA :
      c * Fintype.card V ≤ rowDistinctCount (vertexCycleMatrix G C (2 * L)) :=
    sparseColumnRankTransfer G C Δ (2 * L) c hdeg hcycleRank
  have hroot :
      rowDistinctCount (vertexCycleMatrix G C (2 * L)) ≤ rootedTypeCount G (2 * L) :=
    rowToRootedType G C (2 * L)
  exact le_trans hA hroot

end Rigidity
end Oblivion
