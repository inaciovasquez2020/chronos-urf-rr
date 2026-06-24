import Chronos.Frontier.SelectedDomainDefectTerminalClosureAssumptionDischarge

namespace Chronos
namespace Frontier

structure SelectedDomainRepairDescentComponentTarget : Type where
  repair_descent_statement : Prop
  repair_descent_discharge : repair_descent_statement

structure SelectedDomainZeroDefectReentryComponentTarget
    (repair_descent_statement : Prop) : Type where
  zero_defect_selected_domain_reentry_statement : Prop
  zero_defect_selected_domain_reentry_discharge :
    repair_descent_statement →
      zero_defect_selected_domain_reentry_statement

structure SelectedDomainUnrestrictedTerminalNormalizationComponentTarget
    (zero_defect_selected_domain_reentry_statement : Prop) : Type where
  unrestricted_terminal_normalization_statement : Prop
  unrestricted_terminal_normalization_discharge :
    zero_defect_selected_domain_reentry_statement →
      unrestricted_terminal_normalization_statement

structure SelectedDomainFinalClosureComponentTarget
    (unrestricted_terminal_normalization_statement : Prop) : Type where
  final_closure_statement : Prop
  final_closure_discharge :
    unrestricted_terminal_normalization_statement →
      final_closure_statement

structure SelectedDomainUnrestrictedOblivionClosureComponentTarget
    (final_closure_statement : Prop) : Type where
  unrestricted_oblivion_atom_closure_statement : Prop
  unrestricted_oblivion_atom_closure_discharge :
    final_closure_statement →
      unrestricted_oblivion_atom_closure_statement

structure SelectedDomainDefectSemanticComponentTargets : Type where
  repair_descent_component :
    SelectedDomainRepairDescentComponentTarget
  zero_defect_reentry_component :
    SelectedDomainZeroDefectReentryComponentTarget
      repair_descent_component.repair_descent_statement
  unrestricted_terminal_normalization_component :
    SelectedDomainUnrestrictedTerminalNormalizationComponentTarget
      zero_defect_reentry_component.zero_defect_selected_domain_reentry_statement
  final_closure_component :
    SelectedDomainFinalClosureComponentTarget
      unrestricted_terminal_normalization_component.unrestricted_terminal_normalization_statement
  unrestricted_oblivion_closure_component :
    SelectedDomainUnrestrictedOblivionClosureComponentTarget
      final_closure_component.final_closure_statement

def selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    SelectedDomainDefectTerminalClosureComponentDischarge :=
  { repair_descent_statement :=
      targets.repair_descent_component.repair_descent_statement
    zero_defect_selected_domain_reentry_statement :=
      targets.zero_defect_reentry_component.zero_defect_selected_domain_reentry_statement
    unrestricted_terminal_normalization_statement :=
      targets.unrestricted_terminal_normalization_component.unrestricted_terminal_normalization_statement
    final_closure_statement :=
      targets.final_closure_component.final_closure_statement
    unrestricted_oblivion_atom_closure_statement :=
      targets.unrestricted_oblivion_closure_component.unrestricted_oblivion_atom_closure_statement
    repair_descent_discharge :=
      targets.repair_descent_component.repair_descent_discharge
    zero_defect_selected_domain_reentry_discharge :=
      targets.zero_defect_reentry_component.zero_defect_selected_domain_reentry_discharge
    unrestricted_terminal_normalization_discharge :=
      targets.unrestricted_terminal_normalization_component.unrestricted_terminal_normalization_discharge
    final_closure_discharge :=
      targets.final_closure_component.final_closure_discharge
    unrestricted_oblivion_atom_closure_discharge :=
      targets.unrestricted_oblivion_closure_component.unrestricted_oblivion_atom_closure_discharge }

theorem repair_descent_statement_from_semantic_component_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      targets).repair_descent_statement :=
  repair_descent_theorem_from_component_discharge
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets targets)

theorem zero_defect_selected_domain_reentry_statement_from_semantic_component_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      targets).zero_defect_selected_domain_reentry_statement :=
  zero_defect_selected_domain_reentry_from_component_discharge
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets targets)

theorem unrestricted_terminal_normalization_statement_from_semantic_component_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      targets).unrestricted_terminal_normalization_statement :=
  unrestricted_terminal_normalization_from_component_discharge
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets targets)

theorem final_closure_statement_from_semantic_component_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      targets).final_closure_statement :=
  final_closure_from_component_discharge
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets targets)

theorem unrestricted_oblivion_atom_closure_statement_from_semantic_component_targets
    (targets : SelectedDomainDefectSemanticComponentTargets) :
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets
      targets).unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure_from_component_discharge
    (selected_domain_defect_terminal_closure_component_discharge_from_semantic_targets targets)

end Frontier
end Chronos
