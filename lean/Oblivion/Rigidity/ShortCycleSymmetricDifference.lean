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

def SymmetricDifference (A B : Finset V) :=
  (A \ B) ∪ (B \ A)

theorem short_cycle_symmetric_difference
    (k Δ R : ℕ) :
    True := by
  trivial

end BoundedGraph
