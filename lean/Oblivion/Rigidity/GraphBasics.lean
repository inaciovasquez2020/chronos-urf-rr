namespace Oblivion

structure Graph where
  V : Type
  E : V → V → Prop

def Adj (G : Graph) (u v : G.V) : Prop :=
  G.E u v ∨ G.E v u

def MaxDegreeAtMost (G : Graph) (Δ : Nat) : Prop := True

def Ball (G : Graph) (v : G.V) (R : Nat) : Set G.V :=
  {u | True}

end Oblivion
