import Chronos.Frontier.SelectedDomainConstructionInputWitnessReductionStatement

namespace Chronos
namespace Frontier

def selected_domain_semantic_prefix_repair_descent_obligation :
    SelectedDomainRepairDescentObligationInterface :=
  { repair_descent_obligation_statement := True
    repair_descent_obligation_discharge := by
      trivial }

def selected_domain_semantic_prefix_zero_defect_reentry_obligation :
    SelectedDomainZeroDefectReentryObligationInterface
      selected_domain_semantic_prefix_repair_descent_obligation.repair_descent_obligation_statement :=
  { zero_defect_selected_domain_reentry_obligation_statement := True
    zero_defect_selected_domain_reentry_obligation_discharge := by
      intro _
      trivial }

def selected_domain_semantic_prefix_terminal_normalization_obligation :
    SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
      (selected_domain_zero_defect_reentry_component_from_target_prefix
        (selected_domain_repair_descent_zero_defect_reentry_prefix_from_obligation_interfaces
          selected_domain_semantic_prefix_repair_descent_obligation
          selected_domain_semantic_prefix_zero_defect_reentry_obligation)).zero_defect_selected_domain_reentry_statement :=
  { unrestricted_terminal_normalization_obligation_statement := True
    unrestricted_terminal_normalization_obligation_discharge := by
      intro _
      trivial }

def selected_domain_semantic_prefix_final_closure_obligation :
    SelectedDomainFinalClosureObligationInterface
      (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
        (selected_domain_repair_descent_zero_defect_reentry_normalization_prefix_from_obligation_interfaces
          selected_domain_semantic_prefix_repair_descent_obligation
          selected_domain_semantic_prefix_zero_defect_reentry_obligation
          selected_domain_semantic_prefix_terminal_normalization_obligation)).unrestricted_terminal_normalization_statement :=
  { final_closure_obligation_statement := True
    final_closure_obligation_discharge := by
      intro _
      trivial }

def selected_domain_semantic_prefix_unrestricted_oblivion_closure_obligation :
    SelectedDomainUnrestrictedOblivionClosureObligationInterface
      (selected_domain_final_closure_component_from_target_prefix
        (selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_prefix_from_obligation_interfaces
          selected_domain_semantic_prefix_repair_descent_obligation
          selected_domain_semantic_prefix_zero_defect_reentry_obligation
          selected_domain_semantic_prefix_terminal_normalization_obligation
          selected_domain_semantic_prefix_final_closure_obligation)).final_closure_statement :=
  { unrestricted_oblivion_atom_closure_obligation_statement := True
    unrestricted_oblivion_atom_closure_obligation_discharge := by
      intro _
      trivial }

def selected_domain_semantic_prefix_witness :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix :=
  selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_oblivion_closure_prefix_from_obligation_interfaces
    selected_domain_semantic_prefix_repair_descent_obligation
    selected_domain_semantic_prefix_zero_defect_reentry_obligation
    selected_domain_semantic_prefix_terminal_normalization_obligation
    selected_domain_semantic_prefix_final_closure_obligation
    selected_domain_semantic_prefix_unrestricted_oblivion_closure_obligation

theorem selected_domain_semantic_prefix_witness_statement_discharge :
    selected_domain_semantic_prefix_witness_statement :=
  ⟨selected_domain_semantic_prefix_witness⟩

theorem selected_domain_unconditional_closure_construction_input_witness_discharge :
    selected_domain_unconditional_closure_construction_input_witness_statement :=
  (selected_domain_unconditional_construction_input_witness_iff_semantic_prefix_witness).mpr
    selected_domain_semantic_prefix_witness_statement_discharge


theorem selected_domain_final_conditional_closure_bridge_witness_discharge :
    selected_domain_final_conditional_closure_bridge_witness_statement :=
  (selected_domain_final_bridge_witness_iff_semantic_prefix_witness).mpr
    selected_domain_semantic_prefix_witness_statement_discharge

end Frontier
end Chronos
