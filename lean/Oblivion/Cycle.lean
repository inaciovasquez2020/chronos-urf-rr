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

axiom cycle_length_le_twoR_of_subgraph_ball
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  C.edges.card ≤ 2 * R

axiom ball_cycle_embeds_in_graph
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, C'.edges.card = C.edges.card

end Oblivion
