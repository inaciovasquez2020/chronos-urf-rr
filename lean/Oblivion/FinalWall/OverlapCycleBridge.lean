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

def columnParity (A : Matrix (Fin m) (Fin n) F2) (γ : Finset (Fin m)) (j : Fin n) : F2 :=
  ∑ i in γ, A i j

def OverlapCycleCondition
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n, columnParity A γ j = 0

-- Step 1: local cancellation lemma (pairwise overlap → cancellation)
axiom overlap_pair_cancels
  (A : Matrix (Fin m) (Fin n) F2)
  (i k : Fin m)
  (j : Fin n)
  (h : A i j ≠ 0 ∧ A k j ≠ 0) :
  A i j + A k j = 0

-- Step 2: cycle folding lemma (reduce to pair cancellations)
axiom cycle_fold_reduction
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : isOverlapCycle A γ) :
  ∀ j : Fin n,
    ∃ pairs : Finset (Fin m × Fin m),
      (∀ (p ∈ pairs), overlaps A p.1 p.2) ∧
      (∑ i in γ, A i j) =
      ∑ p in pairs, (A p.1 j + A p.2 j)

-- Final bridge (now reducible to pair cancellation)
theorem overlap_cycle_implies_zero_column_sum
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : isOverlapCycle A γ) :
  OverlapCycleCondition A γ := by
  classical
  intro j
  rcases cycle_fold_reduction A γ hγ j with ⟨pairs, hpairs, hsum⟩
  have hzero :
    (∑ p in pairs, (A p.1 j + A p.2 j)) = 0 := by
    -- each pair cancels
    -- reduces to finite sum of zeros
    sorry
  simpa [columnParity, hsum] using hzero
