import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Nat.Find
import Mathlib.Tactic

namespace Chronos

variable {V : Type} [Fintype V] [DecidableEq V]

def neighbors (adj : V → V → Prop) (v : V) (vs : Finset V) : Finset V :=
  vs.filter (fun u => adj v u)

def bfs_step (adj : V → V → Prop) (s : Finset V) : Finset V :=
  s ∪ (s.bind (fun v => neighbors adj v Finset.univ))

def bfs : (V → V → Prop) → V → Nat → Finset V
  | adj, start, 0 => {start}
  | adj, start, n + 1 => bfs_step adj (bfs adj start n)

def Reachable (adj : V → V → Prop) (x y : V) : Prop :=
  ∃ n, y ∈ bfs adj x n

def dist (adj : V → V → Prop) (x y : V) (h : Reachable adj x y) : Nat :=
  Nat.find h

theorem dist_spec
  (adj : V → V → Prop) (x y : V) (h : Reachable adj x y) :
  y ∈ bfs adj x (dist adj x y h) := by
  exact Nat.find_spec h

theorem bfs_subset_step (adj : V → V → Prop) (s : Finset V) :
  s ⊆ bfs_step adj s := by
  intro x hx
  simp [bfs_step, hx]

theorem bfs_mono (adj : V → V → Prop) (x : V) :
  ∀ n, bfs adj x n ⊆ bfs adj x (n + 1) := by
  intro n
  cases n with
  | zero =>
      intro y hy
      exact bfs_subset_step adj _ hy
  | succ n =>
      intro y hy
      exact bfs_subset_step adj _ hy

theorem mem_bfs_add
  (adj : V → V → Prop) (x y : V) {m n : Nat}
  (h : y ∈ bfs adj x m) :
  y ∈ bfs adj x (m + n) := by
  induction n with
  | zero =>
      simpa using h
  | succ n ih =>
      have h1 : y ∈ bfs adj x (m + n) := ih
      have h2 : y ∈ bfs adj x ((m + n) + 1) := bfs_mono adj x (m + n) h1
      simpa [Nat.add_assoc] using h2

theorem bfs_concat
  (adj : V → V → Prop) {x y z : V} {m n : Nat}
  (hxy : y ∈ bfs adj x m)
  (hyz : z ∈ bfs adj y n) :
  ∃ t ≤ m + n, z ∈ bfs adj x t := by
  refine ⟨m + n, le_rfl, ?_⟩
  have hxymn : y ∈ bfs adj x (m + n) := mem_bfs_add adj x y (n := n) hxy
  induction n generalizing y with
  | zero =>
      simp at hyz
      subst hyz
      simpa using hxymn
  | succ n ih =>
      simp [bfs, bfs_step] at hyz ⊢
      rcases hyz with hz | hz
      · exact ih hxymn hz
      · rcases Finset.mem_bind.mp hz with ⟨u, hu, hzu⟩
        rcases ih hxymn hu with hrec
        exact Or.inr <| Finset.mem_bind.mpr ⟨u, hrec, hzu⟩

theorem reachable_concat
  (adj : V → V → Prop) {x y z : V}
  (hxy : Reachable adj x y)
  (hyz : Reachable adj y z) :
  Reachable adj x z := by
  rcases hxy with ⟨m, hm⟩
  rcases hyz with ⟨n, hn⟩
  rcases bfs_concat adj hm hn with ⟨t, -, ht⟩
  exact ⟨t, ht⟩

theorem dist_triangle
  (adj : V → V → Prop) {x y z : V}
  (hxy : Reachable adj x y)
  (hyz : Reachable adj y z)
  (hxz : Reachable adj x z) :
  dist adj x z hxz ≤ dist adj x y hxy + dist adj y z hyz := by
  rcases bfs_concat adj (dist_spec adj x y hxy) (dist_spec adj y z hyz) with ⟨t, ht_le, hmem⟩
  have hmem' : z ∈ bfs adj x (dist adj x y hxy + dist adj y z hyz) := mem_bfs_add adj x z (n := (dist adj x y hxy + dist adj y z hyz) - t) (by
    simpa [Nat.add_comm, Nat.add_left_comm, Nat.add_assoc, Nat.add_sub_of_le ht_le] using hmem)
  exact Nat.find_min' hxz hmem'

end Chronos
