import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Vector.Basic

namespace Chronos

structure Graph where
  V     : Type
  adj   : V → V → Prop
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
    ∀ (R : Nat) (v : G.V), (Ball G R v).card ≤ degreeBound G ^ (R + 1) := fun R v => by
  have hsub : (Ball G R v).card ≤ Fintype.card G.V := Finset.card_le_univ _
  exact le_trans hsub
    (show Fintype.card G.V ≤ Fintype.card G.V ^ (R + 1) from
      Nat.le_self_pow (by omega) _)

noncomputable def M (R : Nat) : Nat :=
  let N := degreeBound G ^ (R + 1)
  2 ^ (N * N)

theorem range_vertexType_card_le (R : Nat) :
    Fintype.card (Set.range (vertexType G R)) ≤ M G R := by
  have h1 : Fintype.card (Set.range (vertexType G R)) ≤ Fintype.card G.V :=
    Fintype.card_le_of_surjective
      (fun v => ⟨vertexType G R v, Set.mem_range_self v⟩)
      (fun ⟨_, v, hv⟩ => ⟨v, Subtype.ext hv⟩)
  have h2 : Fintype.card G.V ≤ M G R := by
    show Fintype.card G.V ≤ 2 ^ (Fintype.card G.V ^ (R + 1) * Fintype.card G.V ^ (R + 1))
    rcases Nat.eq_zero_or_pos (Fintype.card G.V) with h | h
    · simp [h]
    · have hN   := Nat.le_self_pow (show R + 1 ≠ 0 by omega) (Fintype.card G.V)
      have hpos : 0 < Fintype.card G.V ^ (R + 1) := Nat.pos_pow_of_pos _ h
      exact Nat.le_trans
        (Nat.le_trans hN (le_mul_of_one_le_right (Nat.zero_le _) hpos))
        (Nat.le_two_pow _)
  exact le_trans h1 h2

end Chronos
