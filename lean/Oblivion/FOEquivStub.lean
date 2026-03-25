import Oblivion.CFISkeleton

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  (k = 0)

theorem FO_equiv_base (R : Nat) (G₀ G₁ : Graph) :
  FO_equiv 0 R G₀ G₁ :=
by
  simp [FO_equiv]
