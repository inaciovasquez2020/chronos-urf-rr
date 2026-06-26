import Mathlib.Tactic
import Chronos.Frontier.ConcreteNativeBindingSpec
import Chronos.Frontier.SelectedDomainDefectTerminalClosureAssumptionDischarge
import Chronos.Frontier.SelectedDomainConstructionInputWitnessReductionStatement
import Chronos.Frontier.SelectedDomainSemanticPrefixWitness

namespace Chronos
namespace Frontier

theorem newstein_concrete_binding_tested_against_small_solved_theorems
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    RepositoryNativeNonFactorisationPromotionAllowed concreteNativeBindingSpec ∧
    d.repair_descent_statement ∧
    d.zero_defect_selected_domain_reentry_statement ∧
    d.unrestricted_terminal_normalization_statement ∧
    d.final_closure_statement ∧
    d.unrestricted_oblivion_atom_closure_statement ∧
    selected_domain_unconditional_closure_construction_input_witness_statement ∧
    selected_domain_final_conditional_closure_bridge_witness_statement ∧
    selected_domain_semantic_prefix_witness_statement ∧
    (∃ targetPrefix : SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix,
      (selected_domain_unrestricted_oblivion_closure_component_from_target_prefix targetPrefix).unrestricted_oblivion_atom_closure_statement) := by
  exact ⟨
    concrete_native_nonfactorisation_promotion_allowed,
    repair_descent_theorem_from_component_discharge d,
    zero_defect_selected_domain_reentry_from_component_discharge d,
    unrestricted_terminal_normalization_from_component_discharge d,
    final_closure_from_component_discharge d,
    unrestricted_oblivion_atom_closure_from_component_discharge d,
    selected_domain_unconditional_closure_construction_input_witness_discharge,
    selected_domain_final_conditional_closure_bridge_witness_discharge,
    selected_domain_semantic_prefix_witness_statement_discharge,
    selected_domain_semantic_prefix_unrestricted_oblivion_component_statement_exists
  ⟩

end Frontier
end Chronos
