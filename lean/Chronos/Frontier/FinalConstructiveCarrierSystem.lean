universe u

structure SemanticCore where
  σ : Type u
  α : Type u
  eval : σ → α → ℝ

structure FiniteCarrier (α : Type u) where
  elements : List α
  complete : ∀ x : α, x ∈ elements

structure InfiniteCarrier (α : Type u) : Type u where
  no_finite_witness : ¬ ∃ (_ : FiniteCarrier α), True

def cost (C : SemanticCore) (_p : C.σ) (w : FiniteCarrier C.α) : Nat :=
  w.elements.length

theorem cost_well_defined
  (C : SemanticCore)
  (_p : C.σ)
  (w : FiniteCarrier C.α) :
  cost C _p w = w.elements.length :=
by
  rfl

theorem infinite_exclusion
  (C : SemanticCore)
  (h : InfiniteCarrier C.α) :
  ¬ ∃ w : FiniteCarrier C.α, True :=
by
  exact h.no_finite_witness

def carrier_state (α : Type u) : Type u :=
  Sum (FiniteCarrier α) (InfiniteCarrier α)

def cost_total
  (C : SemanticCore)
  (_p : C.σ)
  (c : FiniteCarrier C.α) : Nat :=
  cost C _p c
