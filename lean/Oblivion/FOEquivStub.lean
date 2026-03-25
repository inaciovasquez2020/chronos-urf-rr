import Oblivion.CFISkeleton

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  (k ≤ 1)

theorem FO_equiv_base (k R : Nat) (G₀ G₁ : Graph) :
  k ≤ 1 → FO_equiv k R G₀ G₁ :=
by
  intro hk
  exact hk
