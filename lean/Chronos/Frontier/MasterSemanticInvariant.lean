import Mathlib.Data.Set.Basic

-- Core semantic base
structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

-- Support definition
def support (B : SemanticBase) (p : B.σ) : Set B.α :=
{ x | B.eval p x ≠ 0 }

-- Kernel equivalence
def ker_equiv (B : SemanticBase) (p q : B.σ) : Prop :=
∀ x, B.eval p x = B.eval q x

-- Semantic zero
def semanticallyZero (B : SemanticBase) (p : B.σ) : Prop :=
∀ x, B.eval p x = 0

-- Master invariant: all layers collapse to same semantic content
theorem MasterSemanticInvariant
  (B : SemanticBase)
  (p q : B.σ) :
  (ker_equiv B p q)
  ↔ (support B p = support B q)
  ↔ (semanticallyZero B p ↔ semanticallyZero B q) :=
by
  constructor
  · intro h
    constructor
    · ext x
      simp [support, h]
    · intro hx
      simp [semanticallyZero, h] at hx
  · intro h x
    have h1 := h.1
    have h2 := h.2
    simpa [ker_equiv]
