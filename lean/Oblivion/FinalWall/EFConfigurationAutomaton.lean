import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic

class EFConfig (σ : Type*) where
  step : σ → σ
  [fintype_state : Fintype σ]
  [dec_state : DecidableEq σ]

attribute [instance] EFConfig.fintype_state EFConfig.dec_state

def reaches {σ : Type*} [EFConfig σ] (s : σ) (t : ℕ) : σ :=
  Nat.iterate EFConfig.step t s

theorem exists_repeat {σ : Type*} [EFConfig σ] (s₀ : σ) :
  ∃ i j : ℕ, i < j ∧ reaches s₀ i = reaches s₀ j := by
  classical
  let N := Fintype.card σ + 1
  have hnotinj : ¬Function.Injective (fun t : Fin N => reaches s₀ t) := by
    intro hinj
    have hcard := Fintype.card_le_of_injective (f := fun t : Fin N => reaches s₀ t) hinj
    simp at hcard
  rcases Finite.exists_ne_map_eq_of_infinite ?_ with ⟨a,b,hab,hEq⟩
  · exact ⟨a,b,by simpa using Fin.lt_iff_val_lt_val.mpr (Nat.lt_of_lt_of_le (Nat.lt_succ_self _) (Nat.le_of_ne hab)), hEq⟩
  · exact Set.Infinite.of_finite (Set.toFinite _)

