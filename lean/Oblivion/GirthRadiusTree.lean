import Oblivion.Graph
import Oblivion.Ball
import Oblivion.CycleMap
import Oblivion.ClosedWalk
import Oblivion.Tree

namespace Oblivion

variable {G : Graph}

/-- RAX: adjacency changes distance by at most 1. -/
lemma RAX_step
    (v : G.V)
    (x y : G.V)
    (hxy : G.Adj x y) :
    dist v y ≤ dist v x + 1 ∧ dist v x ≤ dist v y + 1 := by
  constructor
  · exact dist_le_of_adj_right hxy
  · exact dist_le_of_adj_left hxy

/-- Walk version (layer Lipschitz). -/
lemma RAX_walk
    (v : G.V)
    (W : ClosedWalk G) :
    ∀ ⦃x y⦄, ConsecutiveOn W x y →
      Nat.dist (dist v x) (dist v y) ≤ 1 := by
  intro x y hxy
  obtain ⟨h₁, h₂⟩ := RAX_step (G := G) v x y hxy
  exact Nat.dist_le_iff.mpr ⟨h₁, h₂⟩

/-- Diameter bound for cycles inside a ball. -/
lemma bfs_layer_bound_on_ball_cycle
    (v : G.V)
    (R : Nat)
    (C : ClosedWalk (ball G v R)) :
    cycleDiameter C ≤ 2 * R := by
  classical
  obtain ⟨x, y, hxy⟩ := exists_pair_realizing_cycleDiameter C
  have hx : dist v x.1 ≤ R := x.2
  have hy : dist v y.1 ≤ R := y.2
  have hdist : dist x.1 y.1 ≤ dist v x.1 + dist v y.1 :=
    dist_triangle _ _ _
  have : dist x.1 y.1 ≤ 2 * R := by
    have := add_le_add hx hy
    exact le_trans hdist this
  simpa [hxy] using this

/-- Acyclicity from girth bound. -/
lemma girth_gt_fourR_implies_ball_acyclic
    (v : G.V)
    (R : Nat)
    (hgir : 4 * R < girth G) :
    Acyclic (ball G v R) := by
  intro C
  have hdiam : cycleDiameter C ≤ 2 * R :=
    bfs_layer_bound_on_ball_cycle (G := G) v R C
  have hlen : C.length ≤ 2 * cycleDiameter C :=
    cycle_length_le_two_mul_diameter (G := ball G v R) C C.isCycle
  have hsmall : C.length ≤ 4 * R := by
    omega
  have hbig : girth G ≤ C.length :=
    girth_le_cycle_length (embed_cycle (G := G) v R C)
  omega

/-- Final tree statement. -/
theorem girth_gt_twoR_plus_one_implies_ball_tree
    (v : G.V)
    (R : Nat)
    (hG : Connected G)
    (hgir : 4 * R < girth G) :
    IsTree (ball G v R) := by
  refine ⟨?conn, ?acyc⟩
  · exact connected_ball (G := G) hG v R
  · exact girth_gt_fourR_implies_ball_acyclic (G := G) v R hgir

end Oblivion
