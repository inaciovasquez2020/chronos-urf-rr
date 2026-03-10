import Oblivion.Rigidity.CycleLinearAlgebra
import Oblivion.Rigidity.IncidenceRankBound

namespace Cyclone.CCL.Final

open Cyclone.CCL.Linear
open Cyclone.CCL.Graph

noncomputable section
open Classical

variable {n m : ℕ}

/-- Cycle-overlap rank definition. -/
def COR (A : IncidenceMatrix (n := n) (m := m)) : ℕ :=
  overlapRank A

/-- Final Cyclone/CCL bound: COR controlled by kΔ. -/
theorem cyclone_CCL_bound
    (A : IncidenceMatrix (n := n) (m := m))
    (k Δ : ℕ)
    (h₁ : incidenceRank A ≤ n)
    (h₂ : n ≤ k * Δ) :
    COR A ≤ k * Δ := by
  unfold COR
  have h₃ : overlapRank A ≤ incidenceRank A :=
    overlapRank_le_incidenceRank A
  have h₄ : incidenceRank A ≤ k * Δ :=
    Nat.le_trans h₁ h₂
  exact Nat.le_trans h₃ h₄

end Cyclone.CCL.Final
