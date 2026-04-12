namespace Newstein

class RootedTreeLike (α : Type) where
  root : α
  parent : α → α
  depth : α → Nat
  distG : α → α → Nat
  distT : α → α → Nat
  inBall : α → Prop

variable {α : Type} [RootedTreeLike α]

def depth_G (x : α) : Nat := RootedTreeLike.depth x
def d_G (x y : α) : Nat := RootedTreeLike.distG x y
def d_T (x y : α) : Nat := RootedTreeLike.distT x y
def root_G : α := RootedTreeLike.root
def inBall_R (x : α) : Prop := RootedTreeLike.inBall x

def parentIter : Nat → α → α
  | 0, x => x
  | n + 1, x => RootedTreeLike.parent (parentIter n x)

structure IsRootedShortestPathTree : Prop where
  depth_root :
    depth_G root_G = 0
  dist_root_root :
    d_G root_G root_G = 0
  parent_depth_step :
    ∀ x, x ≠ root_G → depth_G x = depth_G (RootedTreeLike.parent x) + 1
  parent_dist_step :
    ∀ x, x ≠ root_G → d_G root_G x = d_G root_G (RootedTreeLike.parent x) + 1
  parent_eventually_root :
    ∀ x, ∃ n : Nat, parentIter n x = root_G

theorem TreeDepthMetricIdentity
  (hT : IsRootedShortestPathTree) :
  ∀ x, depth_G x = d_G root_G x := by
  intro x
  obtain ⟨n, hn⟩ := hT.parent_eventually_root x
  induction n generalizing x with
  | zero =>
      have hx : x = root_G := hn
      subst hx
      rw [hT.depth_root, hT.dist_root_root]
  | succ n ih =>
      by_cases hx : x = root_G
      · subst hx
        rw [hT.depth_root, hT.dist_root_root]
      · have hpd : depth_G x = depth_G (RootedTreeLike.parent x) + 1 := hT.parent_depth_step x hx
        have hdd : d_G root_G x = d_G root_G (RootedTreeLike.parent x) + 1 := hT.parent_dist_step x hx
        have hparent_root : parentIter n (RootedTreeLike.parent x) = root_G := by
          simpa [parentIter] using hn
        have ih' : depth_G (RootedTreeLike.parent x) = d_G root_G (RootedTreeLike.parent x) := ih (RootedTreeLike.parent x) hparent_root
        rw [hpd, hdd, ih']

structure HasBFSDistEqGraphDist : Prop where
  bfs_dist_eq_graph_dist :
    ∀ x, inBall_R x → d_G root_G x = d_T root_G x

theorem MetricDepthCoincidence
  (hT : IsRootedShortestPathTree)
  (hB : HasBFSDistEqGraphDist) :
  ∀ x, inBall_R x → depth_G x = d_T root_G x := by
  intro x hx
  rw [TreeDepthMetricIdentity hT x]
  rw [hB.bfs_dist_eq_graph_dist x hx]

end Newstein
