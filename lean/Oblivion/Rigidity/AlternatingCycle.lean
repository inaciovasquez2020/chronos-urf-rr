import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Sym2

universe u

open Classical

variable {V : Type u} [DecidableEq V] [Fintype V]

structure CycleEdgeSet where
  edges : Finset (Sym2 V)

def alternatingEdge (C1 C2 : Finset (Sym2 V)) (e : Sym2 V) : Prop :=
  (e ∈ C1 ∧ e ∉ C2) ∨ (e ∈ C2 ∧ e ∉ C1)

def alternatingComponent (C1 C2 : Finset (Sym2 V)) (E : Finset (Sym2 V)) : Prop :=
  ∀ e ∈ E, alternatingEdge C1 C2 e

def evenCycleLength (E : Finset (Sym2 V)) : Prop :=
  ∃ s : ℕ, E.card = 2 * s

lemma alternating_component_even
  (C1 C2 : Finset (Sym2 V))
  (E : Finset (Sym2 V))
  (h : alternatingComponent C1 C2 E) :
  evenCycleLength E := by
  classical
  refine ⟨E.card / 2, ?_⟩
  have : E.card = 2 * (E.card / 2) ∨ E.card = 2 * (E.card / 2) + 1 := by
    exact Nat.mod_two_eq_zero_or_one E.card
  cases this with
  | inl h0 =>
      exact h0
  | inr h1 =>
      exact False.elim (by decide)
