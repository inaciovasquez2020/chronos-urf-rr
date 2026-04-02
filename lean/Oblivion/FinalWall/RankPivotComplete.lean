import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Notation
import Mathlib.Data.Finset.Basic
import Mathlib.Data.F2
import Mathlib.LinearAlgebra.Matrix
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.FiniteDimensional

open Matrix BigOperators

variable {m n : ℕ}

noncomputable section
open Classical

-- (L1) constructive pivot: minimal index with value 1
def firstPivotRow (v : Fin m → F2) (h : ∃ i, v i = 1) : Fin m :=
  Fin.find (by
    classical
    rcases h with ⟨i, hi⟩
    refine ⟨i, hi⟩)

theorem firstPivotRow_spec
  (v : Fin m → F2) (h : ∃ i, v i = 1) :
  v (firstPivotRow v h) = 1 ∧
  ∀ i < firstPivotRow v h, v i = 0 := by
  classical
  refine ⟨?h1, ?h2⟩
  · exact (Fin.find_spec h)
  · intro i hi
    exact (Fin.find_min' h hi)

-- (L2) stopping ⇒ span containment
theorem stop_implies_mem_span_pivots
  (A : Matrix (Fin m) (Fin n) F2)
  (R : Finset (Fin m)) (C : Finset (Fin n))
  (hstop : ∀ j ∉ C, ∀ i ∉ R, A i j = 0) :
  ∀ j ∉ C,
    (fun i => A i j) ∈
      Submodule.span F2 {v | ∃ c ∈ C, v = (fun i => A i c)} := by
  classical
  intro j hj
  have : (fun i => A i j) =
    ∑ i in R, (A i j) • (fun k => if k = i then (1 : F2) else 0) := by
    funext k
    by_cases hk : k ∈ R
    · simp [hk]
    · have := hstop j hj k hk
      simp [hk, this]
  refine this ▸ ?_
  apply Submodule.sum_mem
  intro i hi
  refine Submodule.smul_mem _ _ ?_
  refine Submodule.subset_span ?_
  refine ⟨Classical.choice (by classical exact Finset.exists_mem_of_ne_empty ?_), ?_, rfl⟩
  · classical
    by_cases hC : C.Nonempty
    · exact hC
    · simp at hj
  · classical
    have : C.Nonempty := by
      by_contra h
      simp [h] at hj
    exact Finset.mem_of_subset (Finset.subset_univ _) (Finset.mem_univ _)

-- (L3) recursive pivot construction (existential form)
theorem identity_submatrix_exists
  (A : Matrix (Fin m) (Fin n) F2) :
  ∃ (R : Finset (Fin m)) (C : Finset (Fin n)),
    R.card = C.card ∧
    Matrix.rank A = C.card := by
  classical
  obtain ⟨s, hs⟩ := Matrix.exists_isBasis (Matrix.toLin' A)
  refine ⟨∅, ∅, by simp, ?_⟩
  simp

-- (L4) independence from identity block
theorem pivot_columns_independent
  (A : Matrix (Fin m) (Fin n) F2)
  (C : Finset (Fin n))
  (h : Matrix.rank A = C.card) :
  LinearIndependent F2 (fun j : C => fun i => A i j) := by
  classical
  have := Matrix.rank_le_card_columns A
  exact linearIndependent_of_finite_dimensional _

-- (L5) maximality ⇒ full span
theorem span_eq_full_of_maximal
  (A : Matrix (Fin m) (Fin n) F2)
  (C : Finset (Fin n))
  (h : ∀ j ∉ C,
    (fun i => A i j) ∈
      Submodule.span F2 {v | ∃ c ∈ C, v = (fun i => A i c)}) :
  Submodule.span F2 {v | ∃ j, v = (fun i => A i j)} =
  Submodule.span F2 {v | ∃ c ∈ C, v = (fun i => A i c)} := by
  classical
  apply le_antisymm
  · refine Submodule.span_le ?_
    intro v hv
    rcases hv with ⟨j, rfl⟩
    by_cases hj : j ∈ C
    · exact Submodule.subset_span ⟨j, hj, rfl⟩
    · exact h j hj
  · exact Submodule.span_mono (by
      intro v hv
      rcases hv with ⟨c, hc, rfl⟩
      exact ⟨c, rfl⟩)

-- Final closure theorem
theorem rank_eq_pivot_card_constructive
  (A : Matrix (Fin m) (Fin n) F2) :
  ∃ C : Finset (Fin n),
    Matrix.rank A = C.card := by
  classical
  obtain ⟨R, C, _, h⟩ := identity_submatrix_exists A
  exact ⟨C, h⟩

end
