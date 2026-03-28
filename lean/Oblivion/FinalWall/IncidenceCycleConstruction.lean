import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Finset.Basic

abbrev F2 := ZMod 2

variable {m n : ℕ}

def rowHitsColumn
  (A : Matrix (Fin m) (Fin n) F2)
  (i : Fin m) (j : Fin n) : Prop :=
  A i j ≠ 0

-- Bipartite incidence edges
def IncEdge (A : Matrix (Fin m) (Fin n) F2) :=
  { p : Fin m × Fin n // rowHitsColumn A p.1 p.2 }

-- Closed alternating walk (row → column → row → ...)
structure IncidenceCycle
  (A : Matrix (Fin m) (Fin n) F2) where
  rows   : List (Fin m)
  cols   : List (Fin n)
  length : rows.length = cols.length
  step₁  : ∀ k, k < rows.length → rowHitsColumn A (rows.get ⟨k, by simp⟩) (cols.get ⟨k, by simp⟩)
  step₂  : ∀ k, k < rows.length →
    rowHitsColumn A (rows.get ⟨(k+1) % rows.length, by simp⟩) (cols.get ⟨k, by simp⟩)

-- Projection to γ (rows)
def cycleRows
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A) : Finset (Fin m) :=
  C.rows.toFinset

-- TARGET (now purely combinatorial)
axiom incidence_cycle_even_column_degree
  (A : Matrix (Fin m) (Fin n) F2)
  (C : IncidenceCycle A) :
  ∀ j : Fin n,
    Even (C.rows.countP (fun i => rowHitsColumn A i j))
