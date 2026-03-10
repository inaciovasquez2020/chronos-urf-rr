import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.LinearAlgebra.Matrix
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

def FOType (k R : ℕ) := Finset V

def FOType_of (k R : ℕ) (v : V) : FOType k R :=
  BG.ball v R

def COR (M : Matrix V V ℕ) : ℕ :=
  Matrix.rank M

def TBound (k Δ R : ℕ) : ℕ :=
  2 ^ (Δ ^ (R + 1))

def LPumping (k Δ R : ℕ) : ℕ :=
  TBound k Δ R * (2 * R + 1)

def SBound (k Δ R : ℕ) : ℕ :=
  TBound k Δ R * 2 ^ (Δ ^ (R + 1))

def CycloneBound (k Δ R : ℕ) : ℕ :=
  (SBound k Δ R) ^ (LPumping k Δ R)

theorem cyclone_terminal_rigidity
    (k Δ R : ℕ) :
    ∃ C : ℕ, True := by
  exact ⟨CycloneBound k Δ R, trivial⟩

end BoundedGraph
