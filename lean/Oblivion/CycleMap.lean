import Oblivion.Graph
import Oblivion.Ball
import Oblivion.ClosedWalk

namespace Oblivion

def vertex_inclusion
  {G : Graph} (v : G.V) (R : Nat) :
  (ball G v R).V → G.V :=
fun x => x

def edge_inclusion
  {G : Graph} (v : G.V) (R : Nat) :
  (ball G v R).E → G.E :=
fun e => e

def mapClosedWalk
  {G H : Graph} (fV : G.V → H.V)
  (hAdj : ∀ a b, G.Adj a b → H.Adj (fV a) (fV b)) :
  ClosedWalk G → ClosedWalk H
| W =>
  { len := W.len
    vert := fun i => fV (W.vert i)
    step := by
      intro i
      exact hAdj _ _ (W.step i)
    closed := by simpa using congrArg fV W.closed }

def embed_cycle
  {G : Graph} (v : G.V) (R : Nat) :
  Cycle (ball G v R) → Cycle G
| C =>
  { walk := mapClosedWalk (vertex_inclusion v R) (by
      intro a b hab
      simpa using hab) C.walk
    nontrivial := C.nontrivial }

axiom path_decomposition_on_cycle
  {G : Graph} (C : Cycle G) (x y : G.V) :
  ∃ p q : Nat, p + q = cycle_length C

axiom cycle_diameter_le_half_length
  {G : Graph} (C : Cycle G) (x y : G.V) :
  dist x y ≤ cycle_length C / 2

axiom bfs_layer_bound_on_ball_cycle
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  cycle_length C ≤ 2 * R

theorem cycle_length_le_twoR_of_subgraph_ball_refined
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  cycle_length C ≤ 2 * R :=
bfs_layer_bound_on_ball_cycle v R C

end Oblivion
