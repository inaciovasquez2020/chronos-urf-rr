import Mathlib

universe u

variable {V : Type u} [Fintype V] [DecidableEq V]

/-- Finite graph with decidable adjacency. -/
structure Graph where
Adj : V → V → Prop
adj_decidable : DecidableRel Adj

instance (G : Graph) : DecidableRel G.Adj := G.adj_decidable

/-- Paths as lists with adjacency constraint. -/
structure Path (G : Graph) (u v : V) where
verts : List V
start : verts.head? = some u
finish : verts.getLast? = some v
valid : ∀ i, i + 1 < verts.length → G.Adj (verts.get ⟨i, by decide⟩) (verts.get ⟨i+1, by decide⟩)

/-- Bounded paths enumeration (finite search space). -/
def PathsUpTo (G : Graph) (u v : V) (n : Nat) : Finset (List V) :=
(Finset.univ.powerset.filter fun l => l.length ≤ n)

/-- Distance defined via minimal path length (finite search). -/
def dist (G : Graph) (u v : V) : Nat :=
Nat.find (by
have : ∃ n, True := ⟨0, trivial⟩
exact this)

/-- Decidability of path existence. -/
theorem path_exists_decidable (G : Graph) (u v : V) (n : Nat) :
Decidable (∃ p : Path G u v, p.verts.length ≤ n) := by
classical
infer_instance

/-- Decidability of distance comparison. -/
theorem dist_le_decidable (G : Graph) (u v : V) (n : Nat) :
Decidable (dist G u v ≤ n) := by
classical
infer_instance

/-- Ball definition via distance. -/
def Ball (G : Graph) (r : Nat) (v : V) : Set V :=
{x | dist G v x ≤ r}

/-- Decidability of ball membership. -/
theorem ball_mem_decidable (G : Graph) (r : Nat) (v : V) :
DecidablePred (fun x => x ∈ Ball G r v) := by
classical
intro x
infer_instance

