import Chronos.Frontier.SelectedDomainUnrestrictedOblivionClosureObligationInterface

namespace Chronos
namespace Frontier

/--
A bounded construction target for `defect_atoms`.

This is an interface target, not an unconditional construction of defect atoms.
It records the existence target and the four schema obligations imported from
the already-recorded defect atom obligation matrix.
-/
structure SelectedDomainDefectAtomsConstructionTarget : Type where
  defect_atoms_construction_statement : Prop
  defect_atoms_construction_discharge :
    defect_atoms_construction_statement
  terminal_cardinality_defect_statement : Prop
  terminal_cardinality_of_defect_atoms :
    defect_atoms_construction_statement →
      terminal_cardinality_defect_statement
  selected_domain_reentry_defect_statement : Prop
  zero_defects_imply_selected_domain_reentry :
    defect_atoms_construction_statement →
      selected_domain_reentry_defect_statement
  repair_step_compatibility_defect_statement : Prop
  repair_step_decreases_or_preserves_defect_atoms :
    defect_atoms_construction_statement →
      repair_step_compatibility_defect_statement
  normalization_transfer_defect_statement : Prop
  defect_atoms_transfer_through_terminal_normalization :
    defect_atoms_construction_statement →
      normalization_transfer_defect_statement

/--
The terminal-cardinality obligation follows from the bounded defect-atoms
construction target.
-/
theorem terminal_cardinality_of_defect_atoms_from_construction_target
    (target : SelectedDomainDefectAtomsConstructionTarget) :
    target.terminal_cardinality_defect_statement :=
  target.terminal_cardinality_of_defect_atoms
    target.defect_atoms_construction_discharge

/--
The zero-defect selected-domain reentry obligation follows from the bounded
defect-atoms construction target.
-/
theorem zero_defects_imply_selected_domain_reentry_from_construction_target
    (target : SelectedDomainDefectAtomsConstructionTarget) :
    target.selected_domain_reentry_defect_statement :=
  target.zero_defects_imply_selected_domain_reentry
    target.defect_atoms_construction_discharge

/--
The repair-step compatibility obligation follows from the bounded defect-atoms
construction target.
-/
theorem repair_step_decreases_or_preserves_defect_atoms_from_construction_target
    (target : SelectedDomainDefectAtomsConstructionTarget) :
    target.repair_step_compatibility_defect_statement :=
  target.repair_step_decreases_or_preserves_defect_atoms
    target.defect_atoms_construction_discharge

/--
The terminal-normalization transfer obligation follows from the bounded
defect-atoms construction target.
-/
theorem defect_atoms_transfer_through_terminal_normalization_from_construction_target
    (target : SelectedDomainDefectAtomsConstructionTarget) :
    target.normalization_transfer_defect_statement :=
  target.defect_atoms_transfer_through_terminal_normalization
    target.defect_atoms_construction_discharge

/--
The bounded defect-atoms construction statement itself is exposed as a named
target surface.

Boundary: this does not solve unconditional unrestricted Oblivion Atom closure.
-/
theorem defect_atoms_construction_statement_from_target
    (target : SelectedDomainDefectAtomsConstructionTarget) :
    target.defect_atoms_construction_statement :=
  target.defect_atoms_construction_discharge

end Frontier
end Chronos
