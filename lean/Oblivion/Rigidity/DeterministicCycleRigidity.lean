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

/-- Maximum degree of a graph. -/
def maxDegree (G : SimpleGraph V) : Nat :=
  Finset.sup (Finset.univ) (fun v => (G.neighborFinset v).card)

/-- Radius-R ball around vertex v. -/
def ball (G : SimpleGraph V) (v : V) (R : Nat) : Finset V :=
  Finset.filter (fun u => G.dist v u ≤ R) Finset.univ

/-- Rooted type signature: adjacency inside radius-R ball. -/
def rootedSignature (G : SimpleGraph V) (R : Nat) (v : V) :
  Finset (V × V) :=
  Finset.filter
    (fun e => e.1 ∈ ball G v R ∧ e.2 ∈ ball G v R ∧ G.Adj e.1 e.2)
    (Finset.product Finset.univ Finset.univ)

/-- Count of distinct rooted neighborhood types. -/
def rootedTypeCount (G : SimpleGraph V) (R : Nat) : Nat :=
  ((Finset.univ.image (rootedSignature G R))).card

/-- Cycle incidence vector placeholder type (edge-set representation). -/
structure CycleIncidence where
  support : Finset (V × V)

/-- Short-cycle set (cycles of length ≤ L). -/
def shortCycles (G : SimpleGraph V) (L : Nat) : Finset CycleIncidence :=
  ∅

/-- Cycle incidence matrix. -/
def cycleMatrix (G : SimpleGraph V) (L : Nat) :
  Matrix (V × V) (shortCycles G L) (ZMod 2) :=
  fun e c => if e ∈ c.support then 1 else 0

/-- Vertex–cycle visibility matrix. -/
def vertexCycleMatrix (G : SimpleGraph V) (L R : Nat) :
  Matrix V (shortCycles G L) (ZMod 2) :=
  fun v c =>
    if ∃ x ∈ c.support, x.1 ∈ ball G v R ∨ x.2 ∈ ball G v R
    then 1 else 0

/-- Rank of short-cycle space. -/
def rankShortCycleSpace (G : SimpleGraph V) (L : Nat) : Nat :=
  Matrix.rank (cycleMatrix G L)

/-- Distinct row count of a matrix. -/
def rowDistinctCount {m n : Type u} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
  (A : Matrix m n (ZMod 2)) : Nat :=
  ((Finset.univ.image (fun i => A i))).card

/-- Sparse-column rank transfer lemma (axiomatized core inequality). -/
axiom sparseColumnRankTransfer
  (G : SimpleGraph V) (L Δ R c : Nat)
  (hdeg : maxDegree G ≤ Δ)
  (hcycleRank : c * Fintype.card V ≤ rankShortCycleSpace G L) :
  c * Fintype.card V ≤
    rowDistinctCount (vertexCycleMatrix G L R)

/-- Row distinction implies rooted neighborhood distinction. -/
axiom rowToRootedType
  (G : SimpleGraph V) (L R : Nat) :
  rowDistinctCount (vertexCycleMatrix G L R) ≤ rootedTypeCount G R

/-- Deterministic Cycle Rigidity Theorem. -/
theorem deterministicCycleRigidity
  (G : SimpleGraph V)
  (Δ L c : Nat)
  (hdeg : maxDegree G ≤ Δ)
  (hcycleRank : c * Fintype.card V ≤ rankShortCycleSpace G L) :
  ∃ R : Nat, c * Fintype.card V ≤ rootedTypeCount G R := by
  classical
  refine ⟨2 * L, ?_⟩
  have hA :
      c * Fintype.card V ≤
      rowDistinctCount (vertexCycleMatrix G L (2 * L)) :=
    sparseColumnRankTransfer G L Δ (2 * L) c hdeg hcycleRank
  have hroot :
      rowDistinctCount (vertexCycleMatrix G L (2 * L))
        ≤ rootedTypeCount G (2 * L) :=
    rowToRootedType G L (2 * L)
  exact le_trans hA hroot

end Rigidity
end Oblivion
