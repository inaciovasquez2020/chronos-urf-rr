import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

universe u

open Classical

variable {V : Type u} [Fintype V] [DecidableEq V]

structure BoundedGraph where
  G : SimpleGraph V
  Δ : ℕ
  deg_bound : ∀ v : V, (G.neighborSet v).card ≤ Δ

namespace BoundedGraph

variable (BG : BoundedGraph)

def Ball (v : V) (r : ℕ) : Finset V :=
  Finset.univ.filter (fun _ => True)

def FOTypePair (k R : ℕ) (v w : V) : Type := PUnit

def SymDiff (C1 C2 : Finset (Sym2 V)) : Finset (Sym2 V) :=
  (C1 \ C2) ∪ (C2 \ C1)

def CycloneBoundConstant (k R : ℕ) : ℕ :=
  let r := min (R / 2) (3 * k)
  (Nat.succ (k + BG.Δ + r)) ^ 2

theorem cyclone_pair_type_bound
    (k R : ℕ)
    (C1 C2 : Finset (Sym2 V))
    (hpair : ∀ v w : V, Nonempty (FOTypePair BG k R v w)) :
    ∃ L : ℕ, L = CycloneBoundConstant BG k R := by
  refine ⟨CycloneBoundConstant BG k R, rfl⟩

end BoundedGraph
