import Chronos.Frontier.SelectedDomainFinalConditionalClosureBridge

namespace Chronos
namespace Frontier

/--
The exact remaining unconditional construction input.

An inhabitant of this structure is the missing object needed to pass from the
current verifier-backed conditional toolkit to the selected-domain unrestricted
Oblivion closure surface.

Boundary: this file does not construct such an inhabitant.
-/
structure SelectedDomainUnconditionalClosureConstructionInput : Type where
  final_conditional_closure_bridge :
    SelectedDomainFinalConditionalClosureBridge

/--
Expose the final conditional bridge from the unconditional construction input.
-/
def selected_domain_final_bridge_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    SelectedDomainFinalConditionalClosureBridge :=
  input.final_conditional_closure_bridge

/--
Expose the semantic component bundle from the unconditional construction input.
-/
def selected_domain_semantic_component_targets_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    SelectedDomainDefectSemanticComponentTargets :=
  selected_domain_semantic_component_targets_from_final_bridge
    input.final_conditional_closure_bridge

/--
Expose the defect-atoms construction target from the unconditional construction
input.
-/
def selected_domain_defect_atoms_target_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    SelectedDomainDefectAtomsConstructionTarget :=
  selected_domain_defect_atoms_target_from_final_bridge
    input.final_conditional_closure_bridge

/--
The defect-atoms construction statement follows from the unconditional
construction input.
-/
theorem defect_atoms_construction_statement_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_atoms_target_from_unconditional_construction_input
      input).defect_atoms_construction_statement :=
  defect_atoms_construction_statement_from_final_bridge
    input.final_conditional_closure_bridge

/--
The terminal-cardinality defect obligation follows from the unconditional
construction input.
-/
theorem terminal_cardinality_of_defect_atoms_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_atoms_target_from_unconditional_construction_input
      input).terminal_cardinality_defect_statement :=
  terminal_cardinality_of_defect_atoms_from_final_bridge
    input.final_conditional_closure_bridge

/--
The zero-defect selected-domain reentry defect obligation follows from the
unconditional construction input.
-/
theorem zero_defects_imply_selected_domain_reentry_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_atoms_target_from_unconditional_construction_input
      input).selected_domain_reentry_defect_statement :=
  zero_defects_imply_selected_domain_reentry_from_final_bridge
    input.final_conditional_closure_bridge

/--
The repair-step compatibility defect obligation follows from the unconditional
construction input.
-/
theorem repair_step_decreases_or_preserves_defect_atoms_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_atoms_target_from_unconditional_construction_input
      input).repair_step_compatibility_defect_statement :=
  repair_step_decreases_or_preserves_defect_atoms_from_final_bridge
    input.final_conditional_closure_bridge

/--
The terminal-normalization transfer defect obligation follows from the
unconditional construction input.
-/
theorem defect_atoms_transfer_through_terminal_normalization_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_atoms_target_from_unconditional_construction_input
      input).normalization_transfer_defect_statement :=
  defect_atoms_transfer_through_terminal_normalization_from_final_bridge
    input.final_conditional_closure_bridge

/--
The existing conditional unrestricted Oblivion closure surface follows from the
unconditional construction input.

Boundary: this remains conditional on `input`; it does not construct `input`
and does not prove unconditional unrestricted Oblivion Atom closure.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_unconditional_construction_input
    (input : SelectedDomainUnconditionalClosureConstructionInput) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_unconditional_construction_input
        input)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_final_bridge
    input.final_conditional_closure_bridge

end Frontier
end Chronos
