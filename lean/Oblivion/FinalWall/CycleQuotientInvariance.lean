import Mathlib.LinearAlgebra.Basic

abbrev F2 := ZMod 2

variable {V : Type*}

-- Abstract placeholders
constant Z1 : Type*
constant L_R : Type*
constant quotientDim : Type* → ℕ

-- EF-equivalence placeholder
constant EF_equiv : ℕ → ℕ → Type* → Type* → Prop

-- Axiom: quotient-only invariance
axiom quotient_invariance
  (k R : ℕ) (G₀ G₁ : Type*) :
  EF_equiv k R G₀ G₁ →
  quotientDim G₀ = quotientDim G₁
