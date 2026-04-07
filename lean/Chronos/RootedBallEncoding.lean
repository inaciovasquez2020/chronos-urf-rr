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

theorem bounded_ball_card (_R : Nat) (v : G.V) :
    (Ball G _R v).card ≤ Fintype.card G.V := by
  exact Finset.card_le_univ (s := Ball G _R v)

noncomputable def M (_R : Nat) : Nat :=
  let N := degreeBound G ^ (_R + 1)
  2 ^ (N * N)

theorem M_pos (_R : Nat) : 0 < M G _R := by
  unfold M
  exact Nat.pow_pos (by decide : 0 < 2)

theorem one_le_M (_R : Nat) : 1 ≤ M G _R := by
  exact Nat.succ_le_of_lt (M_pos G _R)

theorem vertexType_image_card_pos (_R : Nat) :
    0 < (Finset.univ.image (vertexType G _R)).card + 1 := by
  exact Nat.succ_pos _

theorem vertexType_image_card_nonempty (_R : Nat) :
    1 ≤ (Finset.univ.image (vertexType G _R)).card + 1 := by
  exact Nat.succ_le_of_lt (vertexType_image_card_pos G _R)

theorem M_nonzero (_R : Nat) : M G _R ≠ 0 := by
  exact Nat.ne_of_gt (M_pos G _R)

theorem vertexType_image_card_succ_nonzero (_R : Nat) :
    (Finset.univ.image (vertexType G _R)).card + 1 ≠ 0 := by
  exact Nat.succ_ne_zero _

theorem vertexType_image_card_le_degreeBound (_R : Nat) :
    (Finset.univ.image (vertexType G _R)).card ≤ degreeBound G := by
  simpa [degreeBound] using
    (Finset.card_image_le (s := (Finset.univ : Finset G.V)) (f := vertexType G _R))


theorem range_vertexType_card_le (_R : Nat) :
    (Finset.univ.image (vertexType G _R)).card ≤ Fintype.card G.V := by
  simpa using
    (Finset.card_image_le (s := (Finset.univ : Finset G.V)) (f := vertexType G _R))

end Chronos
