namespace Newstein

constant Vertex : Type
constant Graph : Type

constant dist : Graph -> Vertex -> Vertex -> Nat
constant InBall : Graph -> Vertex -> Nat -> Vertex -> Prop
constant Parent : Graph -> Vertex -> Vertex -> Prop

def OneStepParentStability (G : Graph) (v : Vertex) (R : Nat) : Prop :=
  ∀ ⦃w p : Vertex⦄,
    InBall G v R w ->
    Parent G p w ->
    InBall G v R p

theorem one_step_parent_stability_interface
    (G : Graph) (v : Vertex) (R : Nat)
    (h : OneStepParentStability G v R) :
    ∀ ⦃w p : Vertex⦄,
      InBall G v R w ->
      Parent G p w ->
      InBall G v R p :=
by
  intro w p hw hp
  exact h hw hp

end Newstein
