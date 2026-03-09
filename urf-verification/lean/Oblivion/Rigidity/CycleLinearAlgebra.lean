import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Data.ZMod.Basic

namespace Cyclone.CCL.Linear

open Classical

abbrev 𝔽₂ := ZMod 2

variable {n m : ℕ}

/-- Binary incidence matrix type. -/
abbrev IncidenceMatrix := Matrix (Fin n) (Fin m) 𝔽₂

/-- Overlap matrix defined from an incidence matrix. -/
def overlapMatrix (A : IncidenceMatrix (n := n) (m := m)) :
    Matrix (Fin n) (Fin n) 𝔽₂ :=
  A * A.transpose

/-- Overlap rank definition. -/
def overlapRank (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  Matrix.rank (overlapMatrix A)

/-- Incidence rank definition. -/
def incidenceRank (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  Matrix.rank A

/-- Fundamental algebraic identity. -/
theorem overlapMatrix_factorization
    (A : IncidenceMatrix (n := n) (m := m)) :
    overlapMatrix A = A * A.transpose := by
  rfl

/-- Rank inequality used in the CCL proof chain. -/
theorem overlapRank_le_incidenceRank
    (A : IncidenceMatrix (n := n) (m := m)) :
    overlapRank A ≤ incidenceRank A := by
  classical
  unfold overlapRank incidenceRank overlapMatrix
  exact Matrix.rank_mul_le_left _ _

end Cyclone.CCL.Linear
