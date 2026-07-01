import Mathlib.Data.Set.Basic
import Chronos.Frontier.SemanticSupportFixedPoint

def ker (σ α : Type) (eval : σ → α → ℝ) : Set σ :=
{ p | ∀ x, eval p x = 0 }

def QuotientSigma (σ : Type) (eval : σ → α → ℝ) :=
σ ⧸ (fun p q => ∀ x, eval p x = eval q x)

theorem support_well_defined
  (σ α : Type) (eval : σ → α → ℝ)
  (p q : σ)
  (h : ∀ x, eval p x = eval q x) :
  { x | eval p x ≠ 0 } = { x | eval q x ≠ 0 } :=
by
  ext x
  simp [h]

theorem ker_support_equiv
  (σ α : Type) (eval : σ → α → ℝ)
  (p : σ) :
  (p ∈ ker σ α eval) ↔ ({ x | eval p x ≠ 0 } = ∅) :=
by
  constructor
  · intro h
    ext x
    simp [ker] at h
    exact h x
  · intro h x
    by_contra hx
    have : x ∈ {x | eval p x ≠ 0} := hx
    simp [h] at this
