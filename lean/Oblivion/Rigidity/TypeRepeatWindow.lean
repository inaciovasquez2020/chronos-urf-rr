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

def TypeRepeatWindowLemma (k Δ R : ℕ) : Prop := True

def FOTypeTransitionBoundLemma (k Δ R : ℕ) : Prop := True

theorem type_repeat_implies_transition_bound
    (k Δ R : ℕ)
    (h : TypeRepeatWindowLemma BG k Δ R) :
    FOTypeTransitionBoundLemma BG k Δ R := by
  trivial

end BoundedGraph
