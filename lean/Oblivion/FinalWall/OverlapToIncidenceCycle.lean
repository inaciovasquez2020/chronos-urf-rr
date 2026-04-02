import Oblivion.FinalWall.IncidenceCycleConstruction
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.Finset.Basic

abbrev F2 := ZMod 2

variable {m n : ℕ}

def rowHitsColumn (A : Matrix (Fin m) (Fin n) F2) (i : Fin m) (j : Fin n) : Prop :=
  A i j ≠ 0

structure OverlapStructure (A : Matrix (Fin m) (Fin n) F2) where
  rows : List (Fin m)
  cols : List (Fin n)
  length_eq : rows.length = cols.length
  step₁ :
    ∀ k, k < rows.length →
      rowHitsColumn A (rows.get ⟨k, by simpa using ‹k < rows.length›⟩)
        (cols.get ⟨k, by simpa [length_eq] using ‹k < rows.length›⟩)
  step₂ :
    ∀ k, k < rows.length →
      rowHitsColumn A
        (rows.get ⟨(k + 1) % rows.length, by
          have hk : rows.length > 0 := by
            cases rows with
            | nil => cases ‹k < rows.length›
            | cons _ _ => simp
          exact Nat.mod_lt _ hk⟩)
        (cols.get ⟨k, by simpa [length_eq] using ‹k < rows.length›⟩)

def buildCycleFromOverlap
  {A : Matrix (Fin m) (Fin n) F2}
  (O : OverlapStructure A) : IncidenceCycle A :=
{ rows := O.rows
  cols := O.cols
  length := O.length_eq
  step₁ := O.step₁
  step₂ := O.step₂ }

theorem overlap_generates_cycle
  {A : Matrix (Fin m) (Fin n) F2}
  (O : OverlapStructure A) :
  ∃ C : IncidenceCycle A, C.rows.toFinset = O.rows.toFinset :=
by
  refine ⟨buildCycleFromOverlap O, rfl⟩

theorem cycle_support_matches_overlap
  {A : Matrix (Fin m) (Fin n) F2}
  (O : OverlapStructure A) :
  cycleRows (buildCycleFromOverlap O) = O.rows.toFinset :=
rfl
