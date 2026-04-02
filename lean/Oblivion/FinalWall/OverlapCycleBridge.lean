import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic

abbrev F2 := ZMod 2

variable {m n : ℕ}

def OverlapCycleCondition
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n, ∑ i in γ, A i j = 0

def IsOverlapCycle
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n,
    Even ((γ.filter fun i => A i j ≠ 0).card)

theorem overlap_cycle_implies_zero_column_sum
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : IsOverlapCycle A γ) :
  OverlapCycleCondition A γ :=
by
  classical
  intro j
  have hEven := hγ j
  have hmod :
    ((γ.filter fun i => A i j ≠ 0).card : F2) = 0 := by
    exact_mod_cast hEven.mod_two_eq_zero
  have :
    ∑ i in γ, A i j =
      ((γ.filter fun i => A i j ≠ 0).card : F2) := by
    classical
    refine Finset.sum_congr rfl ?_
    intro i hi
    by_cases h : A i j = 0
    · simp [h]
    · have : A i j = 1 := by
        have : A i j ≠ 0 := h
        exact one_of_ne_zero this
      simp [h, this]
  simpa [this, hmod]
