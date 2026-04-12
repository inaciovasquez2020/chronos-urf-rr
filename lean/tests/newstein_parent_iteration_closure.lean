namespace Newstein

constant Vertex : Type
constant Graph : Type

constant InBall : Graph -> Vertex -> Nat -> Vertex -> Prop
constant Parent : Graph -> Vertex -> Vertex -> Prop

def ParentIterationClosure (G : Graph) (v : Vertex) (R : Nat) : Prop :=
  ∀ ⦃w p : Vertex⦄,
    InBall G v R w ->
    Parent G p w ->
    InBall G v R p

theorem parent_iteration_closure_interface
    (G : Graph) (v : Vertex) (R : Nat)
    (h : ParentIterationClosure G v R) :
    ∀ ⦃w p : Vertex⦄,
      InBall G v R w ->
      Parent G p w ->
      InBall G v R p :=
by
  intro w p hw hp
  exact h hw hp

end Newstein
