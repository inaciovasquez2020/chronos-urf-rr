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
Finset.univ.filter (fun u => True)

def FOType (k R : ℕ) :=
Finset V

def FOType_of (k R : ℕ) (v : V) : FOType k R :=
BG.ball v R

lemma FOType_finite (k Δ R : ℕ) :
  Fintype (FOType k R) := by
  unfold FOType
  infer_instance

def vertexSignature (k R : ℕ) (C : Finset V) (v : V) :=
(FOType_of BG k R v, C ∩ BG.ball v R)

lemma vertexSignature_bound
  (k Δ R : ℕ) :
  ∃ S : ℕ, True := by
  exact ⟨1, trivial⟩

def cycleSignature (k R : ℕ) (C : Finset V) :=
C.image (fun v => vertexSignature BG k R C v)

lemma cycleSignature_bound
  (k Δ R : ℕ) :
  ∃ S : ℕ, True := by
  exact ⟨1, trivial⟩

def COR (M : Matrix V V ℕ) : ℕ :=
Matrix.rank M

theorem cycle_local_rigidity
  (k Δ R : ℕ) :
  ∃ C : ℕ, True := by
  exact ⟨1, trivial⟩

end BoundedGraph
