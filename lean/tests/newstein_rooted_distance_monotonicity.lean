namespace Newstein

constant Vertex : Type
constant Tree : Type

constant depth : Tree -> Vertex -> Nat
constant Parent : Tree -> Vertex -> Vertex -> Prop

def ParentDepthDecrement (T : Tree) : Prop :=
  ∀ ⦃w p : Vertex⦄,
    Parent T p w ->
    depth T p + 1 = depth T w

def RootedDistanceMonotonicity (T : Tree) : Prop :=
  ∀ ⦃w p : Vertex⦄,
    Parent T p w ->
    depth T p ≤ depth T w

theorem parent_depth_decrement_to_monotonicity
    (T : Tree)
    (h : ParentDepthDecrement T) :
    RootedDistanceMonotonicity T :=
by
  intro w p hp
  have hdp : depth T p + 1 = depth T w := h hp
  omega

end Newstein
