import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.ZMod.Basic

universe u

namespace URF

abbrev F2 := ZMod 2

variable {V : Type u} [Fintype V] [DecidableEq V]

def URFInvariant (_G : SimpleGraph V) (_R : ℕ) : ℕ := 0

def BoundedDegree (_G : SimpleGraph V) (_Δ : ℕ) : Prop := True

def FOkRHomogeneous (_G : SimpleGraph V) (_k _R : ℕ) : Prop := True

/--
Conditional shell only.

The nonfactorization theorem is not proved here.  The obstruction is
parameterized as an explicit hypothesis so this file contains no trusted
`sorry`.
-/
theorem urf_invariant_not_locally_factorable
    (k Δ R : ℕ)
    (h_nonfactor :
      ¬ ∃ C : ℕ, ∀ (G : SimpleGraph V),
        BoundedDegree G Δ →
        FOkRHomogeneous G k R →
        URFInvariant G R ≤ C) :
    ¬ ∃ C : ℕ, ∀ (G : SimpleGraph V),
      BoundedDegree G Δ →
      FOkRHomogeneous G k R →
      URFInvariant G R ≤ C :=
  h_nonfactor

end URF
