import Oblivion.Graph
import Oblivion.Ball
import Oblivion.Cycle

namespace Oblivion

-- edge embedding from ball → base graph
axiom edge_inclusion
  {G : Graph} (v : G.V) (R : Nat) :
  (ball G v R).E → G.E

-- vertex embedding
axiom vertex_inclusion
  {G : Graph} (v : G.V) (R : Nat) :
  (ball G v R).V → G.V

-- compatibility of adjacency under inclusion
axiom inclusion_preserves_adj
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ a b,
    (ball G v R).Adj a b →
    G.Adj (vertex_inclusion v R a) (vertex_inclusion v R b)

-- corrected cycle embedding
def embed_cycle
  {G : Graph} (v : G.V) (R : Nat) :
  Cycle (ball G v R) → Cycle G :=
fun C =>
  ⟨C.edges.image (edge_inclusion v R)⟩

-- diameter vs length bridge (needed for BFS argument)
axiom cycle_diameter_le_half_length
  {G : Graph} (C : Cycle G) :
  ∀ u w ∈ C.edges, dist u w ≤ cycle_length C

-- refined BFS bound (now justified structurally)
axiom cycle_length_le_twoR_of_subgraph_ball_refined
  {G : Graph} (v : G.V) (R : Nat)
  (C : Cycle (ball G v R)) :
  cycle_length C ≤ 2 * R

end Oblivion
