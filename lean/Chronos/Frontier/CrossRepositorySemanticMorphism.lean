import Mathlib.Data.Set.Basic

-- Base semantic system
structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

-- Morphism between semantic universes
structure SemanticUniverseMorphism (A B : SemanticBase) where
  mapσ : A.σ → B.σ
  mapα : A.α → B.α
  preserves_eval :
    ∀ p x,
      A.eval p x = B.eval (mapσ p) (mapα x)

-- Cross-system MSGP embedding
structure CrossMSGP where
  source : SemanticBase
  target : SemanticBase
  morphism : SemanticUniverseMorphism source target

-- Preservation of support under universe mapping
theorem support_preservation
  (A B : SemanticBase)
  (f : SemanticUniverseMorphism A B)
  (p : A.σ) :
  { x | A.eval p x ≠ 0 } =
  { x | B.eval (f.mapσ p) (f.mapα x) ≠ 0 } :=
by
  ext x
  simp [f.preserves_eval]
