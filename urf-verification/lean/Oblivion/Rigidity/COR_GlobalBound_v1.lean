import Mathlib.Tactic
import Oblivion.Rigidity.CycleLinearAlgebra
import Oblivion.Rigidity.CCL_Closure_v1

namespace Cyclone.CCL.Global

open Cyclone.CCL.Linear
open Cyclone.CCL.Closure

variable {n m : ℕ}

/-- Global cycle-overlap rank definition. -/
def COR (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  overlapRank A

/-- Global bound: COR controlled by incidence rank. -/
theorem COR_global_bound
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (h : incidenceRank A ≤ k * Δ) :
    COR A ≤ k * Δ := by
  unfold COR
  exact CCL_closure A k Δ h

end Cyclone.CCL.Global
