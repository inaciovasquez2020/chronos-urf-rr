import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.ZMod.Basic

universe u

namespace URF

abbrev F2 := ZMod 2

variable {V : Type u} [Fintype V] [DecidableEq V]

def URFInvariant (G : SimpleGraph V) (R : ℕ) : ℕ := by
  sorry

def BoundedDegree (G : SimpleGraph V) (Δ : ℕ) : Prop := by
  sorry

def FOkRHomogeneous (G : SimpleGraph V) (k R : ℕ) : Prop := by
  sorry

theorem urf_invariant_not_locally_factorable (k Δ R : ℕ) :
    ¬ ∃ C : ℕ, ∀ (G : SimpleGraph V),
      BoundedDegree G Δ →
      FOkRHomogeneous G k R →
      URFInvariant G R ≤ C := by
  sorry

end URF
