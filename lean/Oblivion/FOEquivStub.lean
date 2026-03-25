import Oblivion.CFISkeleton

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop := True

theorem FO_equiv_refl (k R : Nat) (G : Graph) :
  FO_equiv k R G G := by
  trivial
