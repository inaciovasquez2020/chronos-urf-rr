/-
Discharge package for the selected-domain defect terminal-closure stack.

This file lowers the prior conditional stack from one opaque assumption bundle
to named component proofs.  It still does not construct the semantic repair
objects or `defect_atoms`; it records the exact component package needed to
instantiate the terminal-closure stack assumptions.
-/

import Chronos.Frontier.SelectedDomainDefectTerminalClosureStack

namespace Chronos
namespace Frontier

/--
Named component-discharge package for the selected-domain defect terminal stack.

The component fields match the requested order:
1. repair descent,
2. zero-defect selected-domain reentry,
3. unrestricted terminal normalization,
4. final closure,
5. unrestricted Oblivion Atom closure.
-/
structure SelectedDomainDefectTerminalClosureComponentDischarge : Type where
  repair_descent_statement : Prop
  zero_defect_selected_domain_reentry_statement : Prop
  unrestricted_terminal_normalization_statement : Prop
  final_closure_statement : Prop
  unrestricted_oblivion_atom_closure_statement : Prop
  repair_descent_discharge :
    repair_descent_statement
  zero_defect_selected_domain_reentry_discharge :
    repair_descent_statement ->
      zero_defect_selected_domain_reentry_statement
  unrestricted_terminal_normalization_discharge :
    zero_defect_selected_domain_reentry_statement ->
      unrestricted_terminal_normalization_statement
  final_closure_discharge :
    unrestricted_terminal_normalization_statement ->
      final_closure_statement
  unrestricted_oblivion_atom_closure_discharge :
    final_closure_statement ->
      unrestricted_oblivion_atom_closure_statement

/--
A named component-discharge package constructs the stack assumption package.
-/
def terminal_closure_stack_assumptions_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    SelectedDomainDefectTerminalClosureStackAssumptions where
  repair_descent_theorem_target :=
    d.repair_descent_statement
  zero_defect_selected_domain_reentry_target :=
    d.zero_defect_selected_domain_reentry_statement
  unrestricted_terminal_normalization_target :=
    d.unrestricted_terminal_normalization_statement
  final_closure_target :=
    d.final_closure_statement
  unrestricted_oblivion_atom_closure_target :=
    d.unrestricted_oblivion_atom_closure_statement
  repair_descent_theorem_proof :=
    d.repair_descent_discharge
  zero_defect_selected_domain_reentry_from_repair_descent :=
    d.zero_defect_selected_domain_reentry_discharge
  unrestricted_terminal_normalization_from_zero_defect_reentry :=
    d.unrestricted_terminal_normalization_discharge
  final_closure_from_unrestricted_terminal_normalization :=
    d.final_closure_discharge
  unrestricted_oblivion_atom_closure_from_final_closure :=
    d.unrestricted_oblivion_atom_closure_discharge

/--
The component-discharge package proves repair descent.
-/
theorem repair_descent_theorem_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    d.repair_descent_statement :=
  repair_descent_theorem
    (terminal_closure_stack_assumptions_from_component_discharge d)

/--
The component-discharge package proves zero-defect selected-domain reentry.
-/
theorem zero_defect_selected_domain_reentry_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    d.zero_defect_selected_domain_reentry_statement :=
  zero_defect_selected_domain_reentry
    (terminal_closure_stack_assumptions_from_component_discharge d)

/--
The component-discharge package proves unrestricted terminal normalization.
-/
theorem unrestricted_terminal_normalization_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    d.unrestricted_terminal_normalization_statement :=
  unrestricted_terminal_normalization
    (terminal_closure_stack_assumptions_from_component_discharge d)

/--
The component-discharge package proves final closure.
-/
theorem final_closure_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    d.final_closure_statement :=
  final_closure
    (terminal_closure_stack_assumptions_from_component_discharge d)

/--
The component-discharge package proves unrestricted Oblivion Atom closure.
-/
theorem unrestricted_oblivion_atom_closure_from_component_discharge
    (d : SelectedDomainDefectTerminalClosureComponentDischarge) :
    d.unrestricted_oblivion_atom_closure_statement :=
  unrestricted_oblivion_atom_closure
    (terminal_closure_stack_assumptions_from_component_discharge d)

/--
Audit token for this component-discharge layer.
-/
def selectedDomainDefectTerminalClosureComponentDischargeStatus : String :=
  "COMPONENT_DISCHARGE_PACKAGE_TO_CONDITIONAL_STACK_ASSUMPTIONS"

end Frontier
end Chronos
