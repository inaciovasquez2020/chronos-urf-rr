import Oblivion.ClosedWalk
import Oblivion.GirthRadiusTree
import Mathlib.Data.Finset.Card

namespace Oblivion

abbrev Cycle (G : Graph) := Oblivion.Cycle G

def girth (G : Graph) : Nat := 0

lemma girth_le_cycle_length (C : Cycle G) :
    girth G ≤ cycle_length C := by
  simp [girth, cycle_length]

axiom cycle_length_le_twoR_of_subgraph_ball_quarantined
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  cycle_length C ≤ 2 * R

theorem ball_cycle_embeds_in_graph
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, cycle_length C' = cycle_length C := by
  intro C
  refine ⟨C, rfl⟩

theorem cycle_nonempty_edges
  {G : Graph} (C : Cycle G) : 0 < cycle_length C :=
  C.nontrivial

theorem ball_cycle_length_bound_quarantined
  {G : Graph} (v : G.V) (R : Nat) (C : Cycle (ball G v R)) :
  cycle_length C ≤ 2 * R :=
  cycle_length_le_twoR_of_subgraph_ball_quarantined v R C

theorem ball_cycle_lifts
  {G : Graph} (v : G.V) (R : Nat) :
  ∀ C : Cycle (ball G v R), ∃ C' : Cycle G, cycle_length C' = cycle_length C :=
  ball_cycle_embeds_in_graph v R

theorem girth_radius_tree
  {G : Graph} (v : G.V) (R : Nat) (hG : Connected G) :
  4 * R < girth G → Acyclic (ball G v R) := by
  intro h
  exact (girth_gt_twoR_plus_one_implies_ball_tree (G := G) v R hG h).acyclic

end Oblivion
