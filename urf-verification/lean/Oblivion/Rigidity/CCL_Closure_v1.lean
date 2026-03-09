import Mathlib.Tactic
import Oblivion.Rigidity.CycleLinearAlgebra
import Oblivion.Rigidity.CycloneFinalWall

namespace Cyclone.CCL.Closure

open Cyclone.CCL.Linear
open Cyclone.CCL.Final

variable {n m : ℕ}

/-- One-step closure of the current CCL proof layer. -/
theorem CCL_closure
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (hA : incidenceRank A ≤ k * Δ) :
    overlapRank A ≤ k * Δ := by
  exact cyclone_bound A k Δ hA

end Cyclone.CCL.Closure
