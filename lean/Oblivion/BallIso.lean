import Oblivion.Graph
import Oblivion.Ball
import Mathlib.Data.Bool.Basic

namespace Oblivion

structure BallIso (G H : Graph) (v : G.V) (w : H.V) (R : Nat) : Prop where
  toFun : (ball G v R).V → (ball H w R).V
  invFun : (ball H w R).V → (ball G v R).V
  left_inv : Function.LeftInverse invFun toFun
  right_inv : Function.RightInverse invFun toFun
  adj_iff : ∀ a b, (ball G v R).Adj a b ↔ (ball H w R).Adj (toFun a) (toFun b)

axiom local_potential
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  G.V → Bool

def xorBool : Bool → Bool → Bool
| a, b => decide (a ≠ b)

def lift_map
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  (ball G v R).V → (ball (signedLift (G := G) σ) (v, false) R).V
| u => (u, xorBool false (local_potential σ v R u))

def lift_inv
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  (ball (signedLift (G := G) σ) (v, false) R).V → (ball G v R).V
| u => u.1

axiom lift_map_left_inv
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  Function.LeftInverse (lift_inv σ v R) (lift_map σ v R)

axiom lift_map_right_inv
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  Function.RightInverse (lift_inv σ v R) (lift_map σ v R)

axiom lift_map_adj_iff
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  ∀ a b,
    (ball G v R).Adj a b ↔
    (ball (signedLift (G := G) σ) (v, false) R).Adj (lift_map σ v R a) (lift_map σ v R b)

theorem signedLift_ball_iso_data
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  BallIso G (signedLift (G := G) σ) v (v, false) R := by
  refine ⟨lift_map σ v R, lift_inv σ v R, ?_, ?_, ?_⟩
  · exact lift_map_left_inv σ v R
  · exact lift_map_right_inv σ v R
  · exact lift_map_adj_iff σ v R

end Oblivion
