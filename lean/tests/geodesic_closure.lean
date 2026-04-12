/-
  Scaffold only.
  This file records the exact theorem interface for the Newstein
  geodesic interpolation closure step.
-/

namespace Newstein

constant Vertex : Type
constant Graph : Type

constant dist : Graph -> Vertex -> Vertex -> Nat
constant InBall : Graph -> Vertex -> Nat -> Vertex -> Prop
constant TreePathVertex : Graph -> Vertex -> Vertex -> Vertex -> Prop

/-- Rooted-local tree-convexity hypothesis. -/
def TreeConvexInBall (G : Graph) (v : Vertex) (r R : Nat) : Prop :=
  ∀ ⦃x y w : Vertex⦄,
    InBall G v r x ->
    InBall G v r y ->
    TreePathVertex G x y w ->
    InBall G v R w

/-- Geodesic interpolation closure interface. -/
theorem geodesic_interpolation_closure
    (G : Graph) (v : Vertex) (r R : Nat)
    (hrr : r ≤ R)
    (hconvex : TreeConvexInBall G v r R) :
    ∀ ⦃x y w : Vertex⦄,
      InBall G v r x ->
      InBall G v r y ->
      TreePathVertex G x y w ->
      InBall G v R w :=
by
  intro x y w hx hy hw
  exact hconvex hx hy hw

end Newstein
