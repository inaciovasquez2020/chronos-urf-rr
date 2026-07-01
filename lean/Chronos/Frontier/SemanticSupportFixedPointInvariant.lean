import Chronos.Frontier.SemanticSupportFixedPoint

-- Invariant: semantic zero coincides with empty support
theorem support_fixed_point_invariant
  (σ α : Type) (eval : σ → α → ℝ)
  (p : σ) :
  (∀ x, eval p x = 0) ↔
  ({ x | eval p x ≠ 0 } = (∅ : Set α)) :=
by
  constructor
  · intro h
    ext x
    simp [h]
  · intro h x
    have hx : eval p x = 0 := by
      by_contra hx
      have : x ∈ {x | eval p x ≠ 0} := hx
      simp [h] at this
