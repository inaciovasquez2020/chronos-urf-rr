import Oblivion

structure BaseGraph where
  V : Type
  E : Type

def graph₀ : Graph :=
{ V := Bool,
  E := Unit,
  src := fun _ => false,
  dst := fun _ => true }

def graph₁ : Graph :=
{ V := Bool,
  E := Unit,
  src := fun _ => true,
  dst := fun _ => false }

def CFI (H : BaseGraph) (ε : Bool) : Graph :=
  if ε then graph₁ else graph₀
