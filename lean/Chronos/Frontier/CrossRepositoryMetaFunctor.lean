import Mathlib.Data.Set.Basic

structure SemanticBase where
  σ : Type
  α : Type
  eval : σ → α → ℝ

structure SemanticUniverseMorphism (A B : SemanticBase) where
  mapσ : A.σ → B.σ
  mapα : A.α → B.α
  preserves_eval :
    ∀ p x,
      A.eval p x = B.eval (mapσ p) (mapα x)

-- Meta-level transformation between morphisms
structure MetaMorphism
  {A B C D : SemanticBase}
  (F G : SemanticUniverseMorphism A B → SemanticUniverseMorphism C D) where
  transform :
    ∀ (f : SemanticUniverseMorphism A B),
      F f = G f

-- Identity meta-morphism
def meta_id
  {A B : SemanticBase}
  (F : SemanticUniverseMorphism A B → SemanticUniverseMorphism A B) :
  MetaMorphism F F :=
{ transform := by intro f; rfl }

-- Vertical composition of meta-morphisms
def meta_comp
  {A B C D : SemanticBase}
  {F G H : SemanticUniverseMorphism A B → SemanticUniverseMorphism C D}
  (α : MetaMorphism F G)
  (β : MetaMorphism G H) :
  MetaMorphism F H :=
{ transform := by intro f; rw [α.transform f, β.transform f] }
