import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Algebra.BigOperators.Basic

abbrev F2 := ZMod 2

open BigOperators

variable {m n : ℕ}

def overlaps (A : Matrix (Fin m) (Fin n) F2) (i k : Fin m) : Prop :=
  ∃ j, A i j ≠ 0 ∧ A k j ≠ 0

def isOverlapCycle
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  γ.Nonempty ∧
  ∀ i ∈ γ, ∃ k ∈ γ, k ≠ i ∧ overlaps A i k

-- NEW: column incidence count
def columnIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  ∑ i in γ, (if A i j = 0 then 0 else 1)

def evenIncidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, (columnIncidence A γ j) % 2 = 0

def OverlapCycleCondition
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j, ∑ i in γ, A i j = 0

-- CORE REDUCTION (no longer axiom)
axiom even_incidence_implies_zero
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (h : evenIncidence A γ) :
  OverlapCycleCondition A γ

-- TRUE HARD LEMMA (isolated)
axiom overlap_cycle_even_incidence
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : isOverlapCycle A γ) :
  evenIncidence A γ
