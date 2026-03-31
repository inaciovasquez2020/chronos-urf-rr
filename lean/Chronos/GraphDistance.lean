import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic

namespace Chronos

variable {V : Type} [DecidableEq V]

def neighbors (adj : V → V → Prop) (v : V) (vs : Finset V) : Finset V :=
  vs.filter (fun u => adj v u)

def bfs_step (adj : V → V → Prop) (front visited : Finset V) : Finset V :=
  (front.bind (fun v => neighbors adj v Finset.univ)) \ visited

def bfs (adj : V → V → Prop) (start : V) (fuel : Nat) : Finset V :=
  Nat.rec (Finset.singleton start)
    (fun _ acc => acc ∪ bfs_step adj acc acc)
    fuel

def dist (adj : V → V → Prop) (x y : V) : Nat :=
  Nat.find (fun n => y ∈ bfs adj x n)

end Chronos
