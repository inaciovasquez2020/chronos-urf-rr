import Mathlib.Data.Finset.Basic

namespace Oblivion

universe u
variable {V : Type u} [DecidableEq V]

structure Graph where
  Adj : V → V → Prop

-- Placeholder: cycle as nonempty finite set (to be replaced by edge-set / closed walk model)
def isCycle (G : Graph) (C : Finset V) : Prop :=
  C.Nonempty

def localCycle (G : Graph) (radiusBall : V → Nat → Finset V) (C : Finset V) (R : Nat) : Prop :=
  ∃ v, C ⊆ radiusBall v R

end Oblivion
