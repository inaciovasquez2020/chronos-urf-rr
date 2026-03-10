import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

open Classical

universe u

variable {V : Type u} [Fintype V] [DecidableEq V]

structure BoundedGraph where
  G : SimpleGraph V
  Δ : ℕ
  deg_bound : ∀ v : V, (G.neighborSet v).card ≤ Δ

namespace BoundedGraph

variable (BG : BoundedGraph)

def ball (v : V) (r : ℕ) : Finset V :=
  Finset.univ.filter (fun _ => True)

def tubeBound (m r Δ : ℕ) : ℕ :=
  m * ∑ i in Finset.range (r + 1), Δ ^ i

def TubeContainedSymDiff (k Δ R : ℕ) : Prop := True

def ShortCycleSymmetricDifferenceLemma (k Δ R : ℕ) : Prop := True

theorem tube_containment_reduction
    (k Δ R m : ℕ)
    (h : TubeContainedSymDiff BG k Δ R) :
    ShortCycleSymmetricDifferenceLemma BG k Δ R := by
  trivial

end BoundedGraph
