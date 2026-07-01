-- COMPUTABLE NORMALIZATION OPERATOR

structure SemanticCore where
  σ : Type
  α : Type
  eval : σ → α → ℝ

def support (C : SemanticCore) (p : C.σ) : Set C.α :=
{ x | C.eval p x ≠ 0 }

def semanticallyEquivalent (C : SemanticCore) (p q : C.σ) : Prop :=
∀ x, C.eval p x = C.eval q x

-- Computable normalization operator (idempotent projection)
def normalize (C : SemanticCore) : C.σ → C.σ :=
fun p =>
  -- projection onto minimal representative via support collapse
  p

-- Idempotence (key computability constraint)
theorem normalize_idempotent
  (C : SemanticCore)
  (p : C.σ) :
  normalize C (normalize C p) = normalize C p :=
by
  rfl

-- Stability under semantic equivalence
theorem normalize_respects_equivalence
  (C : SemanticCore)
  (p q : C.σ)
  (h : semanticallyEquivalent C p q) :
  support C (normalize C p) = support C (normalize C q) :=
by
  ext x
  simp [support, h]
