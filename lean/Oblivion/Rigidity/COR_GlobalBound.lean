import Oblivion.Rigidity.CycleLinearAlgebra

namespace Cyclone.CCL.Global

open Cyclone.CCL.Linear

variable {n m : ℕ}

/-- Cycle overlap rank definition. -/
def COR (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  overlapRank A

/-- Global COR bound derived from incidence rank bound. -/
theorem COR_global_bound
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (h : incidenceRank A ≤ k * Δ) :
    COR A ≤ k * Δ := by
  unfold COR
  have h₁ := overlapRank_le_incidenceRank A
  exact Nat.le_trans h₁ h

end Cyclone.CCL.Global
