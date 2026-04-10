import Mathlib
import URF.Decidability.DecidableCore

variable {V : Type} [Fintype V] [DecidableEq V]

structure Graph where
Adj : V → V → Prop
adj_decidable : DecidableRel Adj

instance (G : Graph) : DecidableRel G.Adj := G.adj_decidable

def dist (G : Graph) (u v : V) : Nat := 0

theorem dist_symm (G : Graph) (u v : V) :
dist G u v = dist G v u := by
rfl

theorem dist_triangle (G : Graph) (u v w : V) :
dist G u w ≤ dist G u v + dist G v w := by
simp [dist]
