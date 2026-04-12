namespace Newstein

class RootedTreeLike (α : Type) where
  root : α
  parent : α → α
  depth : α → Nat
  distT : α → α → Nat
  inBall : α → Prop

variable {α : Type} [RootedTreeLike α]

def root_G : α := RootedTreeLike.root
def parent_G (x : α) : α := RootedTreeLike.parent x
def depth_G (x : α) : Nat := RootedTreeLike.depth x
def d_T (x y : α) : Nat := RootedTreeLike.distT x y
def inBall_R (x : α) : Prop := RootedTreeLike.inBall x

structure HasMetricDepthCoincidence : Prop where
  metric_depth_coincidence :
    ∀ x, inBall_R x → depth_G x = d_T root_G x

structure HasParentDistStep : Prop where
  parent_in_ball :
    ∀ x, inBall_R x → inBall_R (parent_G x)
  parent_dist_step :
    ∀ x, x ≠ root_G → inBall_R x → d_T root_G (parent_G x) = d_T root_G x - 1

theorem ParentDepthDecrement
  (hM : HasMetricDepthCoincidence)
  (hP : HasParentDistStep) :
  ∀ x, x ≠ root_G → inBall_R x → depth_G (parent_G x) = depth_G x - 1 := by
  intro x hx hxb
  rw [hM.metric_depth_coincidence (parent_G x) (hP.parent_in_ball x hxb)]
  rw [hM.metric_depth_coincidence x hxb]
  exact hP.parent_dist_step x hx hxb

end Newstein
