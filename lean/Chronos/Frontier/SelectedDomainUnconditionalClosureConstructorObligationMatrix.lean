import Chronos.Frontier.SelectedDomainUnconditionalClosureSolvedFromConstructorTarget

namespace Chronos
namespace Frontier

/--
A bounded constructor-obligation matrix for
`SelectedDomainUnconditionalClosureConstructorTarget`.

It splits the remaining construction into exactly two obligations:

1. `semantic_prefix_constructor_target`;
2. `defect_atoms_constructor_target`.

Boundary: this file does not construct the obligation matrix unconditionally and
does not prove unconditional unrestricted Oblivion Atom closure.
-/
structure SelectedDomainUnconditionalClosureConstructorObligationMatrix : Type where
  semantic_prefix_constructor_statement : Prop
  semantic_prefix_constructor_discharge :
    semantic_prefix_constructor_statement
  semantic_prefix_constructor_target :
    semantic_prefix_constructor_statement ->
      SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix
  defect_atoms_constructor_statement : Prop
  defect_atoms_constructor_discharge :
    defect_atoms_constructor_statement
  defect_atoms_constructor_target :
    defect_atoms_constructor_statement ->
      SelectedDomainDefectAtomsConstructionTarget

/--
Extract the semantic-prefix constructor target from the obligation matrix.
-/
def semantic_prefix_constructor_target_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix :=
  matrix.semantic_prefix_constructor_target
    matrix.semantic_prefix_constructor_discharge

/--
Extract the defect-atoms constructor target from the obligation matrix.
-/
def defect_atoms_constructor_target_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainDefectAtomsConstructionTarget :=
  matrix.defect_atoms_constructor_target
    matrix.defect_atoms_constructor_discharge

/--
Construct `SelectedDomainUnconditionalClosureConstructorTarget` from the split
obligation matrix.
-/
def selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainUnconditionalClosureConstructorTarget :=
  { semantic_prefix_constructor_target :=
      semantic_prefix_constructor_target_from_obligation_matrix
        matrix
    defect_atoms_constructor_target :=
      defect_atoms_constructor_target_from_obligation_matrix
        matrix }

/--
Construct the already named construction input from the obligation matrix.
-/
def selected_domain_unconditional_closure_construction_input_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainUnconditionalClosureConstructionInput :=
  selected_domain_unconditional_closure_construction_input_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
Construct the final conditional bridge from the obligation matrix.
-/
def selected_domain_final_conditional_closure_bridge_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainFinalConditionalClosureBridge :=
  selected_domain_final_conditional_closure_bridge_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
Construct the semantic component targets from the obligation matrix.
-/
def selected_domain_semantic_component_targets_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainDefectSemanticComponentTargets :=
  selected_domain_semantic_component_targets_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
Construct the solved-target surface from the obligation matrix.
-/
def selected_domain_closure_solved_surface_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    SelectedDomainUnconditionalUnrestrictedOblivionAtomClosureSolvedFromConstructorTarget :=
  { constructor_target :=
      selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
        matrix }

/--
The defect-atoms construction statement follows from the obligation matrix.
-/
theorem defect_atoms_construction_statement_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (defect_atoms_constructor_target_from_obligation_matrix
      matrix).defect_atoms_construction_statement :=
  defect_atoms_construction_statement_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
The terminal-cardinality defect obligation follows from the obligation matrix.
-/
theorem terminal_cardinality_of_defect_atoms_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (defect_atoms_constructor_target_from_obligation_matrix
      matrix).terminal_cardinality_defect_statement :=
  terminal_cardinality_of_defect_atoms_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
The zero-defect selected-domain reentry defect obligation follows from the
obligation matrix.
-/
theorem zero_defects_imply_selected_domain_reentry_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (defect_atoms_constructor_target_from_obligation_matrix
      matrix).selected_domain_reentry_defect_statement :=
  zero_defects_imply_selected_domain_reentry_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
The repair-step compatibility defect obligation follows from the obligation
matrix.
-/
theorem repair_step_decreases_or_preserves_defect_atoms_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (defect_atoms_constructor_target_from_obligation_matrix
      matrix).repair_step_compatibility_defect_statement :=
  repair_step_decreases_or_preserves_defect_atoms_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
The terminal-normalization transfer defect obligation follows from the
obligation matrix.
-/
theorem defect_atoms_transfer_through_terminal_normalization_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (defect_atoms_constructor_target_from_obligation_matrix
      matrix).normalization_transfer_defect_statement :=
  defect_atoms_transfer_through_terminal_normalization_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

/--
The selected-domain unrestricted Oblivion closure theorem surface follows from
the constructor-obligation matrix.

Boundary: this is conditional on the matrix; it does not construct the matrix
and does not prove unconditional unrestricted Oblivion Atom closure.
-/
theorem selected_domain_unconditional_unrestricted_oblivion_atom_closure_solved_from_obligation_matrix
    (matrix : SelectedDomainUnconditionalClosureConstructorObligationMatrix) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_obligation_matrix
        matrix)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_constructor_target
    (selected_domain_unconditional_closure_constructor_target_from_obligation_matrix
      matrix)

end Frontier
end Chronos
