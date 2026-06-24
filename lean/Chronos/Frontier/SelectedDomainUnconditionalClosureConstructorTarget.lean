import Chronos.Frontier.SelectedDomainUnconditionalClosureConstructionInput

namespace Chronos
namespace Frontier

/--
A bounded constructor-target interface for
`SelectedDomainUnconditionalClosureConstructionInput`.

This splits the remaining construction input into exactly the two already
named pieces:
1. the five-component semantic prefix;
2. the defect-atoms construction target.

Boundary: this file does not construct the two pieces unconditionally and does
not prove unconditional unrestricted Oblivion Atom closure.
-/
structure SelectedDomainUnconditionalClosureConstructorTarget : Type where
  semantic_prefix_constructor_target :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix
  defect_atoms_constructor_target :
    SelectedDomainDefectAtomsConstructionTarget

/--
Expose the five-component semantic prefix from the constructor target.
-/
def selected_domain_semantic_prefix_from_unconditional_closure_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix :=
  target.semantic_prefix_constructor_target

/--
Expose the defect-atoms construction target from the constructor target.
-/
def selected_domain_defect_atoms_target_from_unconditional_closure_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    SelectedDomainDefectAtomsConstructionTarget :=
  target.defect_atoms_constructor_target

/--
Build the final conditional closure bridge from the split constructor target.
-/
def selected_domain_final_conditional_closure_bridge_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    SelectedDomainFinalConditionalClosureBridge :=
  { semantic_prefix :=
      target.semantic_prefix_constructor_target
    defect_atoms_target :=
      target.defect_atoms_constructor_target }

/--
Build the existing unconditional closure construction input from the split
constructor target.
-/
def selected_domain_unconditional_closure_construction_input_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    SelectedDomainUnconditionalClosureConstructionInput :=
  { final_conditional_closure_bridge :=
      selected_domain_final_conditional_closure_bridge_from_constructor_target
        target }

/--
The semantic component target bundle is obtained from the constructor target via
the final conditional bridge.
-/
def selected_domain_semantic_component_targets_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    SelectedDomainDefectSemanticComponentTargets :=
  selected_domain_semantic_component_targets_from_final_bridge
    (selected_domain_final_conditional_closure_bridge_from_constructor_target
      target)

/--
The defect-atoms construction statement follows from the constructor target.
-/
theorem defect_atoms_construction_statement_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    target.defect_atoms_constructor_target.defect_atoms_construction_statement :=
  defect_atoms_construction_statement_from_target
    target.defect_atoms_constructor_target

/--
The terminal-cardinality defect obligation follows from the constructor target.
-/
theorem terminal_cardinality_of_defect_atoms_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    target.defect_atoms_constructor_target.terminal_cardinality_defect_statement :=
  terminal_cardinality_of_defect_atoms_from_construction_target
    target.defect_atoms_constructor_target

/--
The zero-defect selected-domain reentry defect obligation follows from the
constructor target.
-/
theorem zero_defects_imply_selected_domain_reentry_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    target.defect_atoms_constructor_target.selected_domain_reentry_defect_statement :=
  zero_defects_imply_selected_domain_reentry_from_construction_target
    target.defect_atoms_constructor_target

/--
The repair-step compatibility defect obligation follows from the constructor
target.
-/
theorem repair_step_decreases_or_preserves_defect_atoms_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    target.defect_atoms_constructor_target.repair_step_compatibility_defect_statement :=
  repair_step_decreases_or_preserves_defect_atoms_from_construction_target
    target.defect_atoms_constructor_target

/--
The terminal-normalization transfer defect obligation follows from the
constructor target.
-/
theorem defect_atoms_transfer_through_terminal_normalization_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    target.defect_atoms_constructor_target.normalization_transfer_defect_statement :=
  defect_atoms_transfer_through_terminal_normalization_from_construction_target
    target.defect_atoms_constructor_target

/--
The existing conditional unrestricted Oblivion closure surface follows from the
split constructor target.

Boundary: this remains conditional on the constructor target; it does not prove
unconditional unrestricted Oblivion Atom closure.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_constructor_target
    (target : SelectedDomainUnconditionalClosureConstructorTarget) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_constructor_target
        target)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_final_bridge
    (selected_domain_final_conditional_closure_bridge_from_constructor_target
      target)

end Frontier
end Chronos
