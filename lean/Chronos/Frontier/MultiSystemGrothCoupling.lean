import Mathlib.Data.Set.Basic

-- Base semantic system
structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

-- Support functor
def support (B : SemanticBase) (p : B.σ) : Set B.α :=
{ x | B.eval p x ≠ 0 }

-- Kernel equivalence
def ker_equiv (B : SemanticBase) (p q : B.σ) : Prop :=
∀ x, B.eval p x = B.eval q x

-- Single MSGP object
structure MSGP where
  base : SemanticBase

-- Morphism between MSGP systems
structure MSGPMorphism (A B : MSGP) where
  mapσ : A.base.σ → B.base.σ
  preserves_eval :
    ∀ p x,
      A.base.eval p x = B.base.eval (mapσ p) x

-- Coupled system category
structure MSGPCategory where
  systems : Type
  obj : systems → MSGP
  morphism : ∀ i j : systems, Type
  id : ∀ i, morphism i i
  comp : ∀ {i j k}, morphism j k → morphism i j → morphism i k
