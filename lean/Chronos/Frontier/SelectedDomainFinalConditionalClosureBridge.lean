import Chronos.Frontier.SelectedDomainDefectAtomsConstructionTarget

namespace Chronos
namespace Frontier

/--
A bounded final bridge interface from the five-component semantic prefix plus
the defect-atoms construction target to the existing conditional closure theorem
surface.

This is not an unconditional proof of unrestricted Oblivion Atom closure.
-/
structure SelectedDomainFinalConditionalClosureBridge : Type where
  semantic_prefix :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix
  defect_atoms_target :
    SelectedDomainDefectAtomsConstructionTarget

/--
Extract the repair-descent component from the five-component semantic prefix.
-/
def selected_domain_repair_descent_component_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainRepairDescentComponentTarget :=
  bridge.semantic_prefix.final_closure_prefix.normalization_prefix.zero_defect_reentry_prefix.repair_descent_component

/--
Extract the zero-defect reentry component from the five-component semantic
prefix.
-/
def selected_domain_zero_defect_reentry_component_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainZeroDefectReentryComponentTarget
      (selected_domain_repair_descent_component_from_final_bridge
        bridge).repair_descent_statement :=
  selected_domain_zero_defect_reentry_component_from_target_prefix
    bridge.semantic_prefix.final_closure_prefix.normalization_prefix.zero_defect_reentry_prefix

/--
Extract the unrestricted terminal-normalization component from the
five-component semantic prefix.
-/
def selected_domain_unrestricted_terminal_normalization_component_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainUnrestrictedTerminalNormalizationComponentTarget
      (selected_domain_zero_defect_reentry_component_from_final_bridge
        bridge).zero_defect_selected_domain_reentry_statement :=
  selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
    bridge.semantic_prefix.final_closure_prefix.normalization_prefix

/--
Extract the final-closure component from the five-component semantic prefix.
-/
def selected_domain_final_closure_component_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainFinalClosureComponentTarget
      (selected_domain_unrestricted_terminal_normalization_component_from_final_bridge
        bridge).unrestricted_terminal_normalization_statement :=
  selected_domain_final_closure_component_from_target_prefix
    bridge.semantic_prefix.final_closure_prefix

/--
Extract the unrestricted Oblivion closure component from the five-component
semantic prefix.
-/
def selected_domain_unrestricted_oblivion_closure_component_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainUnrestrictedOblivionClosureComponentTarget
      (selected_domain_final_closure_component_from_final_bridge
        bridge).final_closure_statement :=
  selected_domain_unrestricted_oblivion_closure_component_from_target_prefix
    bridge.semantic_prefix

/--
Build the existing semantic component target bundle from the five-component
semantic prefix.
-/
def selected_domain_semantic_component_targets_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainDefectSemanticComponentTargets :=
  { repair_descent_component :=
      selected_domain_repair_descent_component_from_final_bridge bridge
    zero_defect_reentry_component :=
      selected_domain_zero_defect_reentry_component_from_final_bridge bridge
    unrestricted_terminal_normalization_component :=
      selected_domain_unrestricted_terminal_normalization_component_from_final_bridge bridge
    final_closure_component :=
      selected_domain_final_closure_component_from_final_bridge bridge
    unrestricted_oblivion_closure_component :=
      selected_domain_unrestricted_oblivion_closure_component_from_final_bridge bridge }

/--
Expose the defect-atoms construction target through the final bridge.
-/
def selected_domain_defect_atoms_target_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    SelectedDomainDefectAtomsConstructionTarget :=
  bridge.defect_atoms_target

/--
The defect-atoms construction statement follows from the final bridge.
-/
theorem defect_atoms_construction_statement_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    bridge.defect_atoms_target.defect_atoms_construction_statement :=
  defect_atoms_construction_statement_from_target
    bridge.defect_atoms_target

/--
The existing conditional unrestricted Oblivion closure theorem follows from the
semantic component target bundle extracted from the final bridge.

Boundary: this is still conditional on the final bridge interface. It does not
prove unconditional unrestricted Oblivion Atom closure.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      (selected_domain_semantic_component_targets_from_final_bridge
        bridge)).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_statement_from_semantic_component_targets
    (selected_domain_semantic_component_targets_from_final_bridge bridge)

/--
Terminal-cardinality defect obligation is reachable from the final bridge via
the defect-atoms construction target.
-/
theorem terminal_cardinality_of_defect_atoms_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    bridge.defect_atoms_target.terminal_cardinality_defect_statement :=
  terminal_cardinality_of_defect_atoms_from_construction_target
    bridge.defect_atoms_target

/--
Zero-defect selected-domain reentry defect obligation is reachable from the
final bridge via the defect-atoms construction target.
-/
theorem zero_defects_imply_selected_domain_reentry_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    bridge.defect_atoms_target.selected_domain_reentry_defect_statement :=
  zero_defects_imply_selected_domain_reentry_from_construction_target
    bridge.defect_atoms_target

/--
Repair-step compatibility defect obligation is reachable from the final bridge
via the defect-atoms construction target.
-/
theorem repair_step_decreases_or_preserves_defect_atoms_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    bridge.defect_atoms_target.repair_step_compatibility_defect_statement :=
  repair_step_decreases_or_preserves_defect_atoms_from_construction_target
    bridge.defect_atoms_target

/--
Terminal-normalization transfer defect obligation is reachable from the final
bridge via the defect-atoms construction target.
-/
theorem defect_atoms_transfer_through_terminal_normalization_from_final_bridge
    (bridge : SelectedDomainFinalConditionalClosureBridge) :
    bridge.defect_atoms_target.normalization_transfer_defect_statement :=
  defect_atoms_transfer_through_terminal_normalization_from_construction_target
    bridge.defect_atoms_target

end Frontier
end Chronos
