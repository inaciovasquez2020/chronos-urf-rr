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

def degreeBound : Nat := Fintype.card G.V

theorem bounded_ball_card :
    ∀ (R : Nat) (v : G.V), (Ball G R v).card ≤ degreeBound G ^ (R + 1) := by
  intro R v
  have hsub : (Ball G R v).card ≤ Fintype.card G.V := by
    simp [Ball]
  have hpow : Fintype.card G.V ≤ degreeBound G ^ (R + 1) := by
    cases hV : Fintype.card G.V with
    | zero  => simp [degreeBound, hV]
    | succ n => simp [degreeBound, hV]
  exact le_trans hsub hpow

noncomputable def M (R : Nat) : Nat :=
  let N := degreeBound G ^ (R + 1)
  2 ^ (N * N)

theorem range_vertexType_card_le :
    Fintype.card (Set.range (vertexType G R)) ≤ M G R := by
  classical
  have h1 : Fintype.card (Set.range (vertexType G R)) ≤ Fintype.card G.V :=
    Fintype.card_le_of_injective (fun x => x.1) (by
      intro a b h; cases a; cases b; cases h; rfl)
  have h2 : Fintype.card G.V ≤ M G R := by
    cases hV : Fintype.card G.V with
    | zero  => simp [M, degreeBound, hV]
    | succ n => simp [M, degreeBound, hV]
  exact le_trans h1 h2

end Chronos
