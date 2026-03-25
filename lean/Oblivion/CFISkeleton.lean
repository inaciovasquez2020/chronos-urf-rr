import Oblivion

structure BaseGraph where
  V : Type
  E : Type

noncomputable def CFI (H : BaseGraph) (ε : Bool) : Graph :=
  Classical.choice (Classical.propDecidable True) ▸
  { V := PUnit, E := PUnit,
    src := fun _ => PUnit.unit,
    dst := fun _ => PUnit.unit }
