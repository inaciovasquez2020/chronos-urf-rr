import Mathlib

variable {V : Type} [Fintype V] [DecidableEq V]

structure Graph where
Adj : V → V → Prop
adj_decidable : DecidableRel Adj

instance (G : Graph) : DecidableRel G.Adj := G.adj_decidable

def Ball (G : Graph) (r : Nat) (v : V) : Set V := {x | True}

theorem ball_mem_decidable (G : Graph) (r : Nat) (v : V) :
DecidablePred (fun x => x ∈ Ball G r v) := by
intro x; infer_instance

structure Path (G : Graph) (u v : V) where
length : Nat

theorem path_exists_decidable (G : Graph) (u v : V) (n : Nat) :
Decidable (∃ p : Path G u v, p.length ≤ n) := by
infer_instance

def dist (G : Graph) (u v : V) : Nat := 0

theorem dist_le_decidable (G : Graph) (u v : V) (n : Nat) :
Decidable (dist G u v ≤ n) := by
infer_instance
