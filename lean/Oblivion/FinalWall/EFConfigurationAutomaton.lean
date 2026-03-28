import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.Basic

class EFConfig (σ : Type*) where
  step : σ → σ
  fintype_state : Fintype σ
  dec_state : DecidableEq σ

attribute [instance] EFConfig.fintype_state EFConfig.dec_state

def reaches {σ : Type*} [EFConfig σ] (s : σ) (t : ℕ) : σ :=
  Nat.iterate EFConfig.step t s

theorem exists_repeat_nat {σ : Type*} [EFConfig σ] (s₀ : σ) :
  ∃ i j : ℕ, i < j ∧ reaches s₀ i = reaches s₀ j := by
  classical
  let N := Fintype.card σ + 1
  have :
    ¬ Function.Injective (fun t : Fin N => reaches s₀ t) := by
    intro h
    have hle := Fintype.card_le_of_injective _ h
    simp at hle
  rcases Finite.exists_ne_map_eq_of_infinite ?_ with ⟨i,j,hij,hEq⟩
  · exact ⟨i, j, by simpa using hij, hEq⟩
  · exact Set.infinite_univ
