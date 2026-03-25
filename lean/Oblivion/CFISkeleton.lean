import Oblivion

structure BaseGraph where
  V : Type
  E : Type

-- minimal nontrivial graph (2 vertices, 1 edge)
def trivialGraph : Graph :=
{ V := Bool,
  E := Unit,
  src := fun _ => false,
  dst := fun _ => true }

def CFI (H : BaseGraph) (ε : Bool) : Graph :=
  trivialGraph
