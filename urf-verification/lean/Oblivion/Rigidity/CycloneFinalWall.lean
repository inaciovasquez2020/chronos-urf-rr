import Mathlib.Tactic
import Oblivion.Rigidity.CycleLinearAlgebra
import Oblivion.Rigidity.FundamentalCycleBound

namespace Cyclone.CCL.Final

open Cyclone.CCL.Linear

variable {n m : ℕ}

/-- Abstract COR definition using incidence matrices. -/
def COR (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  overlapRank A

/-- Final wall inequality used in the CCL proof chain. -/
theorem cyclone_bound
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (h : incidenceRank A ≤ k * Δ) :
    COR A ≤ k * Δ := by
  unfold COR
  have h₁ := overlapRank_le_incidenceRank A
  exact Nat.le_trans h₁ h

end Cyclone.CCL.Final
