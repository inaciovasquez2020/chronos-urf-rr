import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Oblivion.Rigidity.CycleLinearAlgebra

namespace Cyclone.CCL.Graph

open Cyclone.CCL.Linear

noncomputable section
open Classical

variable {n m : ℕ}

/-- Rank of an incidence matrix cannot exceed number of rows. -/
theorem incidenceRank_le_rows
    (A : IncidenceMatrix (n := n) (m := m)) :
    incidenceRank A ≤ n := by
  classical
  unfold incidenceRank
  simpa using Matrix.rank_le_card_height A

/-- Graph bound used in the Cyclone reduction. -/
theorem incidenceRank_le_kDelta
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (h : n ≤ k * Δ) :
    incidenceRank A ≤ k * Δ := by
  have h₁ := incidenceRank_le_rows (A := A)
  exact Nat.le_trans h₁ h

end Cyclone.CCL.Graph
