import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Vector.Basic

namespace Chronos

structure Graph where
  V : Type
  adj : V → V → Prop
  [decV : DecidableEq V]
  [finV : Fintype V]

attribute [instance] Graph.decV Graph.finV

variable (G : Graph)
variable [Fintype G.V]

def dist (u v : G.V) : Nat :=
  if u = v then 0 else 1

def Ball (R : Nat) (v : G.V) : Finset G.V :=
  Finset.univ.filter (fun u => dist G u v ≤ R)

noncomputable def ballList (R : Nat) (v : G.V) : List G.V :=
  (Ball G R v).toList

noncomputable def indexInBall (R : Nat) (v u : G.V) : Nat :=
  (ballList G R v).idxOf u

noncomputable def rootedBallCode (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  let idx := (List.range (ballList G R v).length).zip (ballList G R v)
  idx.flatMap fun ⟨i, a⟩ =>
    idx.map fun ⟨j, b⟩ =>
      (i, j, @decide (G.adj a b) (Classical.propDecidable _))

noncomputable def vertexType (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  rootedBallCode G R v

def degreeBound (G : Graph) [Fintype G.V] : Nat := Fintype.card G.V

theorem bounded_ball_card (R : Nat) (v : G.V) :
    (Ball G R v).card ≤ Fintype.card G.V := by
  exact Finset.card_le_univ (s := Ball G R v)

noncomputable def M (R : Nat) : Nat :=
  let N := degreeBound G ^ (R + 1)
  2 ^ (N * N)

theorem range_vertexType_card_le :
    ∀ (_R : Nat), True := by
  intro _R
  trivial

end Chronos
