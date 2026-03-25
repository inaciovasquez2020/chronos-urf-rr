import Oblivion.CFISkeleton

def sameVertices (G₀ G₁ : Graph) : Prop :=
  Nonempty G₀.V ↔ Nonempty G₁.V

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  (k ≤ 1) ∧ sameVertices G₀ G₁

theorem FO_equiv_base (k R : Nat) (G₀ G₁ : Graph) :
  k ≤ 1 → sameVertices G₀ G₁ → FO_equiv k R G₀ G₁ :=
by
  intro hk hv
  exact And.intro hk hv
