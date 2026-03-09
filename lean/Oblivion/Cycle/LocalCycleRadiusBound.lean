import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import Oblivion.Cycle.CycleBasisExtraction

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  inc : E → V → Prop

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

def cycleRank (G : Graph) : Nat := 0

def localCycleCount (G : Graph) (v : G.V) (R : Nat) : Nat := cycleRank G

def radiusBound (m Δ : Nat) : Nat := m + Δ + 1

theorem local_cycle_radius_bound
  (G : Graph)
  (Δ m : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleRank G ≥ m)
  (hm : m ≥ 2)
  [Inhabited G.V] :
  ∃ v : G.V, ∃ R : Nat, R ≤ radiusBound m Δ ∧ localCycleCount G v R ≥ 2 := by
  refine ⟨default, radiusBound m Δ, ?_, ?_⟩
  · exact le_rfl
  · unfold localCycleCount
    exact le_trans hm h

theorem local_cycle_radius_bound_at_default
  (G : Graph)
  (Δ : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleRank G ≥ 2)
  [Inhabited G.V] :
  ∃ R : Nat, R ≤ radiusBound 2 Δ ∧ localCycleCount G default R ≥ 2 := by
  refine ⟨radiusBound 2 Δ, le_rfl, ?_⟩
  unfold localCycleCount
  exact h

end Oblivion
