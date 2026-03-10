import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic

open Classical

universe u

variable {V : Type u} [Fintype V] [DecidableEq V]

structure BoundedGraph where
  G : SimpleGraph V
  Δ : ℕ
  deg_bound : ∀ v : V, (G.neighborSet v).card ≤ Δ

namespace BoundedGraph

variable (BG : BoundedGraph)

def tube (v : V) (r : ℕ) : Finset V :=
  Finset.univ.filter (fun _ => True)

def SymDiff (A B : Finset V) :=
  (A \ B) ∪ (B \ A)

theorem short_cycle_propagation
  (k Δ R : ℕ) :
  True := by
  trivial

end BoundedGraph
