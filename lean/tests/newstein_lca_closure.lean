namespace Newstein

constant Vertex : Type
constant Graph : Type

constant InBall : Graph -> Vertex -> Nat -> Vertex -> Prop
constant Ancestor : Graph -> Vertex -> Vertex -> Prop
constant OnTreePath : Graph -> Vertex -> Vertex -> Vertex -> Prop

def ParentClosure (G : Graph) (v : Vertex) (R : Nat) : Prop :=
  ∀ ⦃w p : Vertex⦄,
    InBall G v R w ->
    Ancestor G p w ->
    InBall G v R p

def AncestorDescentClosure (G : Graph) (v : Vertex) (R : Nat) : Prop :=
  ∀ ⦃u w z : Vertex⦄,
    InBall G v R u ->
    InBall G v R w ->
    Ancestor G u w ->
    OnTreePath G u w z ->
    InBall G v R z

theorem parent_to_ancestor_descent
    (G : Graph) (v : Vertex) (R : Nat)
    (h : ParentClosure G v R) :
    AncestorDescentClosure G v R :=
by
  intro u w z hu hw hanc hz
  exact hu

end Newstein
