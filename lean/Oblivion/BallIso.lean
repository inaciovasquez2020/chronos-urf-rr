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

-- replaced by constructive LocalPotential
#check Oblivion.local_potential_of_tree
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

-- pending: derive from XOR involution
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  Function.LeftInverse (lift_inv σ v R) (lift_map σ v R)

-- pending: derive from XOR involution
  {G : Graph} (σ : G.E → Bool) (v : G.V) (R : Nat) :
  Function.RightInverse (lift_inv σ v R) (lift_map σ v R)

-- pending: derive from tree_potential parity consistency
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


namespace Oblivion

variable {G : Graph}

def zeroSigning (G : Graph) : G.E → Bool := fun _ => false

lemma xor_four_cancel (a b c d : Bool) (h : c ^^^ d = a ^^^ b) :
    (a ^^^ c) ^^^ (b ^^^ d) = false := by
  cases a <;> cases b <;> cases c <;> cases d <;> simp at h ⊢
  all_goals cases h

lemma xor_involutive (a b : Bool) : (a ^^^ b) ^^^ b = a := by
  cases a <;> cases b <;> decide

def lift_map
    (σ : G.E → Bool)
    (v : G.V)
    (R : Nat)
    (φ : G.V → Bool) :
    (signedLift (G := G) σ).V → (signedLift (G := G) (zeroSigning G)).V :=
  fun x => (x.1, x.2 ^^^ φ x.1)

def lift_map_inv
    (σ : G.E → Bool)
    (v : G.V)
    (R : Nat)
    (φ : G.V → Bool) :
    (signedLift (G := G) (zeroSigning G)).V → (signedLift (G := G) σ).V :=
  fun x => (x.1, x.2 ^^^ φ x.1)

lemma lift_map_left_inv
    (σ : G.E → Bool)
    (v : G.V)
    (R : Nat)
    (φ : G.V → Bool) :
    Function.LeftInverse
      (lift_map_inv (G := G) σ v R φ)
      (lift_map (G := G) σ v R φ) := by
  intro x
  cases x with
  | mk u b =>
    simp [lift_map, lift_map_inv, xor_involutive]

lemma lift_map_right_inv
    (σ : G.E → Bool)
    (v : G.V)
    (R : Nat)
    (φ : G.V → Bool) :
    Function.RightInverse
      (lift_map_inv (G := G) σ v R φ)
      (lift_map (G := G) σ v R φ) := by
  intro x
  cases x with
  | mk u b =>
    simp [lift_map, lift_map_inv, xor_involutive]

lemma lift_map_adj_iff_to_trivial
    (σ : G.E → Bool)
    (v : G.V)
    (R : Nat)
    (φ : G.V → Bool)
    (hφ : ∀ e : G.E, φ e.1.1 ^^^ φ e.1.2 = σ e)
    (x y : (signedLift (G := G) σ).V) :
    (signedLift (G := G) σ).Adj x y ↔
    (signedLift (G := G) (zeroSigning G)).Adj
      (lift_map (G := G) σ v R φ x)
      (lift_map (G := G) σ v R φ y) := by
  cases x with
  | mk x bx =>
    cases y with
    | mk y by =>
      simp [signedLift, lift_map, zeroSigning, hφ]

end Oblivion
