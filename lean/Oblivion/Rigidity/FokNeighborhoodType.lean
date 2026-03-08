import Mathlib.Combinatorics.SimpleGraph.Basic
import Oblivion.Rigidity.NeighborhoodBalls

namespace Oblivion

universe u

def RootedBallIso {V : Type u} [DecidableEq V]
    (G : SimpleGraph V) (v w : V) (R : Nat) : Prop :=
  Nonempty (({x // x ∈ ballSet G v R}) ≃ ({x // x ∈ ballSet G w R}))

def FO_k_R_Homogeneous {V : Type u} [DecidableEq V]
    (G : SimpleGraph V) (k R : Nat) : Prop :=
  ∀ v w : V, RootedBallIso G v w R

theorem FO_k_R_Homogeneous.refl {V : Type u} [DecidableEq V]
    (G : SimpleGraph V) (k R : Nat) (h : FO_k_R_Homogeneous G k R) (v : V) :
    RootedBallIso G v v R := by
  exact h v v

end Oblivion
