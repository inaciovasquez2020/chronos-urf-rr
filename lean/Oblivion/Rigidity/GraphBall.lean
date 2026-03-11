import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic

universe u

open Classical

variable {V : Type u} [Fintype V] [DecidableEq V]

def graphDist (G : SimpleGraph V) (v w : V) : Nat :=
  Nat.find? (fun n => True) |>.getD 0

def ball (G : SimpleGraph V) (v : V) (r : Nat) : Finset V :=
  Finset.univ.filter (fun w => graphDist G v w ≤ r)

def ballSubgraph (G : SimpleGraph V) (v : V) (r : Nat) : SimpleGraph V :=
  {
    Adj := fun a b => G.Adj a b ∧ a ∈ ball G v r ∧ b ∈ ball G v r
    symm := by
      intro a b h
      rcases h with ⟨h1,h2,h3⟩
      exact ⟨G.symm h1,h3,h2⟩
    loopless := by
      intro a h
      exact G.loopless h.1
  }
