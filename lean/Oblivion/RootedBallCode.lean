import Oblivion.EFEquiv
import Mathlib.Data.Finset.Basic

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def adjacent (G : Graph) (v w : G.V) : Prop :=
  ∃ e : G.E, (G.src e = v ∧ G.dst e = w) ∨ (G.src e = w ∧ G.dst e = v)

inductive Reachable (G : Graph) : Nat → G.V → G.V → Prop
| refl (v : G.V) : Reachable G 0 v v
| step {R : Nat} {v w u : G.V} :
    Reachable G R v w → adjacent G w u → Reachable G (R + 1) v u

def Ball (G : Graph) (R : Nat) (v : G.V) : Set G.V :=
  fun w => ∃ r ≤ R, Reachable G r v w

def rootedBallCode (G : Graph) [Fintype G.V] [DecidableEq G.V] (R : Nat) (v : G.V) : Finset G.V :=
  (Finset.univ.filter fun w => decide (w ∈ Ball G R v))

class RadiusRCode (G : Graph) [Fintype G.V] [DecidableEq G.V] where
  code : Nat → G.V → Finset G.V

instance (G : Graph) [Fintype G.V] [DecidableEq G.V] : RadiusRCode G where
  code R v := rootedBallCode G R v
