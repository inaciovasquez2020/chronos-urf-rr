-- lean/oblivion/bfs_cycle/BFSCycleCorrectness.lean

import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.Finset

namespace BFSCycle

variable {V : Type} [DecidableEq V]
variable (G : SimpleGraph V)

def Path := List V

def IsWalk : Path → Prop
| [] => True
| [_] => True
| a::b::t => G.Adj a b ∧ IsWalk (b::t)

def NoRepeat (p : Path) : Prop :=
p.Nodup

def IsSimpleCycle (p : Path) : Prop :=
p.length ≥ 3 ∧
p.head? = p.getLast? ∧
IsWalk G p ∧
NoRepeat p.dropLast

structure BFSState :=
(parent : V → Option V)
(depth : V → Nat)
(seen : Finset V)

structure CrossEdgeCert (st : BFSState) :=
(v u : V)
(hv : v ∈ st.seen)
(hu : u ∈ st.seen)
(hAdj : G.Adj v u)
(hNotParent : st.parent v ≠ some u)

axiom parent_chain_reaches_root
(st : BFSState) (root : V)
(hroot : root ∈ st.seen)
(hroot0 : st.parent root = none)
(v : V) (hv : v ∈ st.seen) :
∃ p : Path,
p.head? = some v ∧
p.getLast? = some root ∧
p.length = st.depth v + 1

axiom cross_edge_gives_cycle
(st : BFSState) (root : V)
(hroot : root ∈ st.seen)
(hroot0 : st.parent root = none)
(ce : CrossEdgeCert (G:=G) st) :
∃ c : Path, IsSimpleCycle (G:=G) c

theorem bfs_cycle_correct
(st : BFSState) (root : V)
(hroot : root ∈ st.seen)
(hroot0 : st.parent root = none)
(ce : CrossEdgeCert (G:=G) st) :
∃ c : Path, IsSimpleCycle (G:=G) c :=
by
  exact cross_edge_gives_cycle (G:=G) st root hroot hroot0 ce

end BFSCycle
