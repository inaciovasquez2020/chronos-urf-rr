import Mathlib.Data.Set.Basic

-- Fixed point: evaluation → support → kernel collapse structure
structure SupportFixedPoint (σ α : Type) (eval : σ → α → ℝ) where

  support : σ → Set α :=
    fun p => { x | eval p x ≠ 0 }

  semanticallyZero : σ → Prop :=
    fun p => ∀ x, eval p x = 0

  ker : Set σ :=
    { p | ∀ x, eval p x = 0 }

  stability :
    ∀ p : σ,
      semanticallyZero p ↔ support p = ∅

  additivity :
    ∀ p q : σ,
      support (p + q) = support p ∪ support q

  quotient_invariance :
    ∀ p q : σ,
      (∀ x, eval p x = eval q x) →
      support p = support q
