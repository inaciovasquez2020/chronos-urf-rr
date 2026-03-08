import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Set.Finite
import Mathlib.Order.Iterate
import Mathlib.Tactic

open Function

namespace Oblivion

universe u

variable {V : Type u} [DecidableEq V]

def neighborSet (G : SimpleGraph V) (S : Set V) : Set V :=
  {v | ∃ u ∈ S, G.Adj u v}

def ballSet (G : SimpleGraph V) (v : V) : Nat → Set V
  | 0 => {x | x = v}
  | Nat.succ R => ballSet G v R ∪ neighborSet G (ballSet G v R)

theorem self_mem_ballSet (G : SimpleGraph V) (v : V) (R : Nat) :
    v ∈ ballSet G v R := by
  induction R with
  | zero =>
      simp [ballSet]
  | succ R ih =>
      simp [ballSet, ih]

theorem mono_ballSet (G : SimpleGraph V) (v : V) :
    ∀ R, ballSet G v R ⊆ ballSet G v (R + 1) := by
  intro R x hx
  simp [ballSet, hx]

theorem adj_mem_ballSet_succ {G : SimpleGraph V} {v x y : V} {R : Nat}
    (hx : x ∈ ballSet G v R) (hxy : G.Adj x y) :
    y ∈ ballSet G v (R + 1) := by
  simp [ballSet, hx, hxy]

end Oblivion
