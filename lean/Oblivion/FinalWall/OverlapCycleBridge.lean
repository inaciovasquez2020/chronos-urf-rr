import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic

abbrev F2 := ZMod 2

open BigOperators

variable {m n : ℕ}

def overlaps (A : Matrix (Fin m) (Fin n) F2) (i k : Fin m) : Prop :=
  ∃ j, A i j ≠ 0 ∧ A k j ≠ 0

def columnIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  ∑ i in γ, if A i j = 0 then 0 else 1

def evenIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, (columnIncidence A γ j) % 2 = 0

def incidenceDegree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  columnIncidence A γ j

def balancedOverlap
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n,
    Even (∑ i in γ, if A i j = 0 then 0 else 1)

def OverlapCycleCondition
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, ∑ i in γ, A i j = 0

lemma balancedOverlap_implies_evenIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : balancedOverlap A γ) :
  evenIncidence A γ := by
  intro j
  rcases hγ j with ⟨k, hk⟩
  exact Nat.modEq_zero_iff_dvd.mpr ⟨k, by simpa [columnIncidence] using hk.symm⟩

axiom even_incidence_implies_zero
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (h : evenIncidence A γ) :
  OverlapCycleCondition A γ

axiom overlap_cycle_even_degree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : balancedOverlap A γ) :
  ∀ j, Even (incidenceDegree A γ j)

theorem balanced_overlap_implies_zero_column_sum
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : balancedOverlap A γ) :
  OverlapCycleCondition A γ :=
  even_incidence_implies_zero A γ (balancedOverlap_implies_evenIncidence A γ hγ)
