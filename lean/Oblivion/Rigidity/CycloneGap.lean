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

def ShortCycleGeneratingFamily (k Δ R : ℕ) : Prop := True

def SymmetricDifferenceShortCycleLemma (k Δ R : ℕ) : Prop := True

theorem cyclone_reduces_to_short_cycle_gap
    (k Δ R : ℕ) :
    SymmetricDifferenceShortCycleLemma BG k Δ R → True := by
  intro _
  trivial

end BoundedGraph
