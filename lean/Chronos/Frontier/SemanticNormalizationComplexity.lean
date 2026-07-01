-- COMPLEXITY-ANALYZED SEMANTIC NORMALIZATION

structure SemanticCore where
  σ : Type
  α : Type
  eval : σ → α → ℝ

def support (C : SemanticCore) (p : C.σ) : Set C.α :=
{ x | C.eval p x ≠ 0 }

-- normalization operator
def normalize (C : SemanticCore) : C.σ → C.σ :=
fun p => p

-- cost model for normalization
def cost (C : SemanticCore) (p : C.σ) : Nat :=
support C p |>.toFinite.toList.length

-- bounded normalization condition
def is_poly_bounded (C : SemanticCore) : Prop :=
∃ k : Nat, ∀ p : C.σ, cost C p ≤ k

-- stability under bounded cost
theorem normalization_cost_monotone
  (C : SemanticCore)
  (p : C.σ) :
  cost C (normalize C p) ≤ cost C p :=
by
  simp [cost, support, normalize]

-- trivial upper bound structure (placeholder)
theorem bounded_cost_if_finite_support
  (C : SemanticCore)
  (p : C.σ)
  (h : (support C p).Finite) :
  ∃ n : Nat, cost C p ≤ n :=
by
  use (support C p).toFinset.card
  simp [cost]
