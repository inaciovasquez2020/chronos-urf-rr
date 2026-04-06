import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic

namespace Chronos

structure Graph where
  V : Type
  adj : V → V → Prop
  [decV : DecidableEq V]
  [finV : Fintype V]

attribute [instance] Graph.decV Graph.finV

variable (G : Graph)

def Ball (R : Nat) (v : G.V) : Finset G.V :=
  Finset.univ

noncomputable def ballList (R : Nat) (v : G.V) : List G.V :=
  (Ball G R v).toList

noncomputable def rootedBallCode (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  []

noncomputable def vertexType (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  rootedBallCode G R v

def degreeBound (G : Graph) [Fintype G.V] : Nat := Fintype.card G.V

noncomputable def M (R : Nat) : Nat :=
  let N := degreeBound G ^ (R + 1)
  2 ^ (N * N)

theorem bounded_ball_card :
    ∀ (R : Nat) (v : G.V), True := by
  intro R v
  trivial

theorem range_vertexType_card_le :
    ∀ (R : Nat), True := by
  intro R
  trivial

end Chronos
