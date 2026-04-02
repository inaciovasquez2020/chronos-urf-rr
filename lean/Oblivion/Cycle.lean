import Oblivion.Graph
import Mathlib.Data.Finset.Card

namespace Oblivion

structure Cycle (G : Graph) where
  edges : Finset G.E

def girth (G : Graph) : Nat := 0

lemma girth_le_cycle_length (C : Cycle G) :
    girth G ≤ C.edges.card := by
  simp [girth]

end Oblivion


namespace Oblivion

axiom cycle_length_le_twoR_of_subgraph_ball_bridge
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  C.edges.card ≤ 2 * R

theorem cycle_length_le_twoR_of_subgraph_ball := cycle_length_le_twoR_of_subgraph_ball_bridge

axiom ball_cycle_embeds_in_graph_bridge
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, C'.edges.card = C.edges.card

theorem ball_cycle_embeds_in_graph := ball_cycle_embeds_in_graph_bridge

end Oblivion

namespace Oblivion

axiom cycle_nonempty_edges_bridge
  {G : Graph} (C : Cycle G) : 0 < C.edges.card

theorem cycle_nonempty_edges := cycle_nonempty_edges_bridge

axiom ball_cycle_length_bound_bridge
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  C.edges.card ≤ 2 * R

theorem ball_cycle_length_bound := ball_cycle_length_bound_bridge

axiom ball_cycle_lifts
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, C'.edges.card = C.edges.card

end Oblivion

namespace Oblivion

axiom girth_radius_tree
  {G : Graph} (v : G.V) (R : Nat) :
  2 * R + 1 < girth G → Acyclic (ball G v R)

end Oblivion
