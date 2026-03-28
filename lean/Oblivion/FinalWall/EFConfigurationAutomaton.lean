import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic

class EFConfig (σ : Type*) where
  step : σ → σ
  fintype_state : Fintype σ
  dec_state : DecidableEq σ

attribute [instance] EFConfig.fintype_state EFConfig.dec_state

def reaches {σ : Type*} [EFConfig σ] (s : σ) (t : ℕ) : σ :=
  Nat.iterate EFConfig.step t s

theorem exists_repeat {σ : Type*} [EFConfig σ] (s₀ : σ) :
  ∃ i j : Fin (Fintype.card σ + 1), i < j ∧ reaches s₀ i = reaches s₀ j := by
  classical
  let f : Fin (Fintype.card σ + 1) → σ := fun t => reaches s₀ t
  have hnotinj : ¬ Function.Injective f := by
    intro hinj
    have hle := Fintype.card_le_of_injective f hinj
    simp at hle
  exact Finite.not_injective_iff_exists_lt_eq.mp hnotinj

theorem exists_repeat_nat {σ : Type*} [EFConfig σ] (s₀ : σ) :
  ∃ i j : ℕ, i < j ∧ reaches s₀ i = reaches s₀ j := by
  rcases exists_repeat s₀ with ⟨i, j, hij, hEq⟩
  exact ⟨i, j, hij, hEq⟩
