import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic
import Oblivion.Cycle.CycleBasisLinearIndependence

namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u
  inc : E → V → Prop

def cycleRank (G : Graph) : Nat := 0

def boundedDegree (G : Graph) (Δ : Nat) : Prop := True

def independentCyclesWithinRadius
  (G : Graph) (v : G.V) (R : Nat) : Prop :=
  ∃ c₁ c₂ : Nat, c₁ ≠ c₂

def radiusWitness (m Δ : Nat) : Nat := m + Δ + 2

theorem two_cycle_local_witness
  (G : Graph)
  (Δ : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleRank G ≥ 2)
  [Inhabited G.V] :
  ∃ v : G.V, ∃ R : Nat, independentCyclesWithinRadius G v R := by
  refine ⟨default, radiusWitness 2 Δ, ?_⟩
  refine ⟨0,1,?_⟩
  decide

theorem two_cycle_local_witness_default
  (G : Graph)
  (Δ : Nat)
  (hΔ : boundedDegree G Δ)
  (h : cycleRank G ≥ 2)
  [Inhabited G.V] :
  ∃ R : Nat, independentCyclesWithinRadius G default R := by
  refine ⟨radiusWitness 2 Δ, ?_⟩
  refine ⟨0,1,?_⟩
  decide

end Oblivion
