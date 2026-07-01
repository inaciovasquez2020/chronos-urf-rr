import Mathlib.Data.Set.Basic

structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

def support (B : SemanticBase) (p : B.σ) : Set B.α :=
{ x | B.eval p x ≠ 0 }

def semanticallyZero (B : SemanticBase) (p : B.σ) : Prop :=
∀ x, B.eval p x = 0

-- Attractor equivalence class (all stable states)
def AttractorClass (B : SemanticBase) : Set B.σ :=
{ p | semanticallyZero B p ∨ support B p ≠ ∅ }

-- Canonical minimal attractor condition:
def is_minimal_attractor (B : SemanticBase) (p : B.σ) : Prop :=
semanticallyZero B p ∧ support B p = ∅

-- Uniqueness of canonical attractor
theorem minimal_attractor_unique
  (B : SemanticBase)
  (p q : B.σ)
  (hp : is_minimal_attractor B p)
  (hq : is_minimal_attractor B q) :
  support B p = support B q :=
by
  simp [is_minimal_attractor] at *
  rw [hp.2, hq.2]
  rfl

-- Collapse theorem: minimal attractor implies full semantic collapse
theorem attractor_collapse
  (B : SemanticBase)
  (p : B.σ)
  (h : is_minimal_attractor B p) :
  ∀ x, B.eval p x = 0 :=
by
  intro x
  exact h.1 x
