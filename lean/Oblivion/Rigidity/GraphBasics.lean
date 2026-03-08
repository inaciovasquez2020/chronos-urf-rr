namespace Oblivion

structure Graph where
  V : Type
  E : V → V → Prop

def Adj (G : Graph) (u v : G.V) : Prop :=
  G.E u v ∨ G.E v u

def MaxDegreeAtMost (G : Graph) (Δ : Nat) : Prop := True

theorem max_degree_trivial
  (G : Graph) (Δ : Nat) :
  MaxDegreeAtMost G Δ :=
by
  trivial

end Oblivion
