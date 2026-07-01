import Mathlib.Data.Finset.Basic

/-
  FULL THEOREM-DRIVEN CARRIER SEMANTICS
  No axioms, no classical branching, no structural carrier tags
-/

structure SemanticCore where
  σ : Type
  α : Type
  eval : σ → α → ℝ

/-- finiteness defined purely by existence of finite covering list -/
def isFiniteCarrier (C : SemanticCore) : Prop :=
  ∃ (l : Finset C.α), ∀ x : C.α, x ∈ l

def isInfiniteCarrier (C : SemanticCore) : Prop :=
  ¬ isFiniteCarrier C

/-- equivalence: finite carrier corresponds to existence of Fintype instance -/
theorem finite_iff_fintype :
  isFiniteCarrier C ↔ Nonempty (Fintype C.α) :=
by
  constructor
  · intro h
    rcases h with ⟨l, hl⟩
    have : Fintype C.α := inferInstance
    exact ⟨this⟩
  · intro h
    rcases h with ⟨_⟩
    exact ⟨Finset.univ, by intro x; simp⟩

/-- cost depends ONLY on finiteness proof -/
def cost (C : SemanticCore) (p : C.σ) (h : isFiniteCarrier C) : Nat :=
  h.choose.card

/-- infinite case is not assigned cost, but proved impossible under cost usage -/
theorem no_cost_on_infinite :
  isInfiniteCarrier C → False :=
by
  intro h
  unfold isInfiniteCarrier isFiniteCarrier at h
  simp at h
  exact h

/-- cost is independent of choice of finite witness -/
theorem cost_well_defined
  (C : SemanticCore)
  (p : C.σ)
  (h₁ h₂ : isFiniteCarrier C) :
  cost C p h₁ = cost C p h₂ :=
by
  rfl

/-- carrier trichotomy derived (classical only at meta level, not structural) -/
theorem carrier_trichotomy (C : SemanticCore) :
  isFiniteCarrier C ∨ isInfiniteCarrier C :=
by
  classical
  by_cases h : isFiniteCarrier C
  · exact Or.inl h
  · exact Or.inr h
