-- MINIMAL SEMANTIC CORE SYSTEM

structure SemanticCore where
  σ : Type
  α : Type
  eval : σ → α → ℝ

-- SINGLE primitive invariant (everything collapses into this)
def invariant (C : SemanticCore) : Prop :=
∀ p q : C.σ,
  (∀ x, C.eval p x = C.eval q x)
  ↔
  ({ x | C.eval p x ≠ 0 } = { x | C.eval q x ≠ 0 })

-- canonical semantic zero
def sem_zero (C : SemanticCore) (p : C.σ) : Prop :=
∀ x, C.eval p x = 0

-- support definition (derived object)
def support (C : SemanticCore) (p : C.σ) : Set C.α :=
{ x | C.eval p x ≠ 0 }

-- collapse theorem: everything reduces to eval equivalence
theorem semantic_core_collapse
  (C : SemanticCore)
  (p q : C.σ)
  (h : invariant C) :
  (∀ x, C.eval p x = C.eval q x)
  ↔
  (support C p = support C q) :=
by
  simpa [support, invariant] using h p q
