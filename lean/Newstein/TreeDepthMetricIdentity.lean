namespace Newstein

class RootedTreeLike (α : Type) where
  root : α
  parent : α → α
  depth : α → Nat
  dist : α → α → Nat

variable {α : Type} [RootedTreeLike α]

def depth_G (x : α) : Nat := RootedTreeLike.depth x
def d_G (x y : α) : Nat := RootedTreeLike.dist x y
def parent_G (x : α) : α := RootedTreeLike.parent x
def root_G : α := RootedTreeLike.root

def parentIter : Nat → α → α
  | 0, x => x
  | n + 1, x => parent_G (parentIter n x)

structure IsRootedShortestPathTree : Prop where
  depth_root :
    depth_G root_G = 0
  dist_root_root :
    d_G root_G root_G = 0
  parent_depth_step :
    ∀ x, x ≠ root_G → depth_G x = depth_G (parent_G x) + 1
  parent_dist_step :
    ∀ x, x ≠ root_G → d_G root_G x = d_G root_G (parent_G x) + 1
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
      · have hpd : depth_G x = depth_G (parent_G x) + 1 := hT.parent_depth_step x hx
        have hdd : d_G root_G x = d_G root_G (parent_G x) + 1 := hT.parent_dist_step x hx
        have hparent_root : parentIter n (parent_G x) = root_G := by
          simpa [parentIter] using hn
        have ih' : depth_G (parent_G x) = d_G root_G (parent_G x) := ih (parent_G x) hparent_root
        rw [hpd, hdd, ih']

end Newstein
