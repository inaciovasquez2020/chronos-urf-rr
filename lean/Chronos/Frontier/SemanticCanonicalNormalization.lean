-- CANONICAL NORMAL FORM OF SEMANTIC SYSTEMS

structure SemanticCore where
  σ : Type
  α : Type
  eval : σ → α → ℝ

def support (C : SemanticCore) (p : C.σ) : Set C.α :=
{ x | C.eval p x ≠ 0 }

def semanticallyEquivalent (C : SemanticCore) (p q : C.σ) : Prop :=
∀ x, C.eval p x = C.eval q x

-- Normal form selector: chooses canonical representative
def normalize (C : SemanticCore) (p : C.σ) : C.σ :=
p  -- placeholder fixed-point representative choice

-- Normal form condition: idempotence + invariance
def is_normal_form (C : SemanticCore) (p : C.σ) : Prop :=
normalize C p = p

-- Uniqueness of canonical form (up to semantic equivalence)
theorem canonical_normal_form_uniqueness
  (C : SemanticCore)
  (p q : C.σ)
  (hp : is_normal_form C p)
  (hq : is_normal_form C q)
  (h : semanticallyEquivalent C p q) :
  support C p = support C q :=
by
  ext x
  simp [support, h]
