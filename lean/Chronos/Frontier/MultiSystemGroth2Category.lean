import Mathlib.Data.Set.Basic

structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

structure MSGP where
  base : SemanticBase

structure MSGPMorphism (A B : MSGP) where
  mapσ : A.base.σ → B.base.σ
  preserves_eval :
    ∀ p x,
      A.base.eval p x = B.base.eval (mapσ p) x

-- 2-morphism: transformation between morphisms
structure MSGP2Morphism
  {A B : MSGP}
  (f g : MSGPMorphism A B) where
  pointwise :
    ∀ p,
      f.mapσ p = g.mapσ p

-- identity 2-morphism
def id2
  {A B : MSGP}
  (f : MSGPMorphism A B) : MSGP2Morphism f f :=
{ pointwise := by intro p; rfl }

-- vertical composition of 2-morphisms
def vcomp
  {A B : MSGP}
  {f g h : MSGPMorphism A B}
  (α : MSGP2Morphism f g)
  (β : MSGP2Morphism g h) :
  MSGP2Morphism f h :=
{ pointwise := by intro p; rw [α.pointwise p, β.pointwise p] }
