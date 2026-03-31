import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Vector

namespace Chronos

structure Graph where
  V : Type
  adj : V → V → Prop
  [decV : DecidableEq V]
  [finV : Fintype V]

attribute [instance] Graph.decV Graph.finV

variable (G : Graph)

axiom dist : G.V → G.V → Nat

def Ball (R : Nat) (v : G.V) : Finset G.V :=
  Finset.univ.filter (fun u => dist G u v ≤ R)

def ballList (R : Nat) (v : G.V) : List G.V :=
  (Ball G R v).toList

def indexInBall (R : Nat) (v u : G.V) : Nat :=
  (ballList G R v).idxOf u

def rootedBallCode (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  ((ballList G R v).enum.bind fun ⟨i,a⟩ =>
    (ballList G R v).enum.map fun ⟨j,b⟩ =>
      (i, j, decide (G.adj a b)))

def vertexType (R : Nat) (v : G.V) : List (Nat × Nat × Bool) :=
  rootedBallCode G R v

axiom degreeBound : Nat
axiom bounded_ball_card :
  ∀ (R : Nat) (v : G.V), (Ball G R v).card ≤ degreeBound G ^ (R + 1)

noncomputable def M (R : Nat) : Nat :=
  let N := degreeBound G ^ (R + 1)
  2 ^ (N * N)

axiom range_vertexType_card_le :
  Fintype.card (Set.range (vertexType G R)) ≤ M G R

end Chronos
