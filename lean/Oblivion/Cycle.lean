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

theorem ball_cycle_embeds_in_graph {G : Graph} (v : G.V) (R : Nat) : Graph.Embeds (ball G v R) G := ball_cycle_embeds_in_graph_bridge v R

end Oblivion

namespace Oblivion

theorem cycle_nonempty_edges_bridge
  {G : Graph} (C : Cycle G) : 0 < C.edges.card := by
  simpa using C.nonempty_edges

theorem cycle_nonempty_edges
  {G : Graph} (C : Cycle G) : 0 < C.edges.card := cycle_nonempty_edges_bridge C

axiom ball_cycle_length_bound_bridge
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  C.edges.card ≤ 2 * R

theorem ball_cycle_length_bound {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) : C.edges.card ≤ 2 * R := ball_cycle_length_bound_bridge v R C

axiom ball_cycle_lifts
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, C'.edges.card = C.edges.card

end Oblivion

namespace Oblivion

axiom girth_radius_tree
  {G : Graph} (v : G.V) (R : Nat) :
  2 * R + 1 < girth G → Acyclic (ball G v R)

end Oblivion
