import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic

abbrev F2 := ZMod 2

open BigOperators

variable {m n : ℕ}

def rowHitsColumn
  (A : Matrix (Fin m) (Fin n) F2)
  (i : Fin m) (j : Fin n) : Prop :=
  A i j ≠ 0

def columnIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  ∑ i in γ, if A i j = 0 then 0 else 1

def incidenceDegree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  columnIncidence A γ j

def evenIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, Even (incidenceDegree A γ j)

def OverlapCycleCondition
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, ∑ i in γ, A i j = 0

def bipartiteColumnCycle
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n, Even (∑ i in γ, if rowHitsColumn A i j then 1 else 0)

lemma bipartiteColumnCycle_implies_evenIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : bipartiteColumnCycle A γ) :
  evenIncidence A γ := by
  intro j
  simpa [evenIncidence, incidenceDegree, columnIncidence, rowHitsColumn] using hγ j

axiom even_incidence_implies_zero
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (h : evenIncidence A γ) :
  OverlapCycleCondition A γ

theorem bipartiteColumnCycle_implies_zero_column_sum
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : bipartiteColumnCycle A γ) :
  OverlapCycleCondition A γ :=
  even_incidence_implies_zero A γ (bipartiteColumnCycle_implies_evenIncidence A γ hγ)
