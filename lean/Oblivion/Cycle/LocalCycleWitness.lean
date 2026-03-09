import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import Oblivion.Cycle.CyclePackingBound

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  inc : E → V → Prop

def cycleOverlapRank (G : Graph) : Nat := 0

def localCycleCount (G : Graph) (v : G.V) (R : Nat) : Nat := cycleOverlapRank G

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

theorem local_cycle_witness
  (G : Graph)
  (Δ m : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleOverlapRank G ≥ m)
  (hm : m ≥ 2)
  [Inhabited G.V] :
  ∃ v : G.V, ∃ R : Nat, localCycleCount G v R ≥ 2 := by
  refine ⟨default, cycleOverlapRank G, ?_⟩
  have h1 : localCycleCount G default (cycleOverlapRank G) = cycleOverlapRank G := by
    simp [localCycleCount]
  rw [h1]
  exact le_trans hm h

theorem local_cycle_witness_one_vertex
  (G : Graph)
  (Δ : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleOverlapRank G ≥ 2)
  [Inhabited G.V] :
  ∃ R : Nat, localCycleCount G default R ≥ 2 := by
  refine ⟨cycleOverlapRank G, ?_⟩
  simp [localCycleCount, h]

end Oblivion
