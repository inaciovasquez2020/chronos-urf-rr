import Chronos.Frontier.SelectedDomainUnrestrictedTerminalNormalizationObligationInterface

namespace Chronos
namespace Frontier

/--
A bounded obligation interface for exactly one semantic component target:
`SelectedDomainFinalClosureComponentTarget`.

The interface is dependent on the unrestricted terminal-normalization statement,
matching the existing dependent semantic component target stack.
-/
structure SelectedDomainFinalClosureObligationInterface
    (unrestricted_terminal_normalization_statement : Prop) : Type where
  final_closure_obligation_statement : Prop
  final_closure_obligation_discharge :
    unrestricted_terminal_normalization_statement →
      final_closure_obligation_statement

/--
Bridge from the bounded final-closure obligation interface to the existing
dependent final-closure semantic component target.
-/
def selected_domain_final_closure_component_target_from_obligation_interface
    {unrestricted_terminal_normalization_statement : Prop}
    (iface :
      SelectedDomainFinalClosureObligationInterface
        unrestricted_terminal_normalization_statement) :
    SelectedDomainFinalClosureComponentTarget
      unrestricted_terminal_normalization_statement :=
  { final_closure_statement :=
      iface.final_closure_obligation_statement
    final_closure_discharge :=
      iface.final_closure_obligation_discharge }

/--
A four-component prefix of the existing dependent semantic component target
stack, extending the repair-descent + zero-defect reentry + terminal-normalization
prefix by exactly one new target: final closure.
-/
structure SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureTargetPrefix : Type where
  normalization_prefix :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationTargetPrefix
  final_closure_obligation :
    SelectedDomainFinalClosureObligationInterface
      (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
        normalization_prefix).unrestricted_terminal_normalization_statement

/--
Bridge the four-component prefix into the existing dependent semantic component
target stack shape by constructing the final-closure component target over the
prefix unrestricted terminal-normalization statement.
-/
def selected_domain_final_closure_component_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureTargetPrefix) :
    SelectedDomainFinalClosureComponentTarget
      (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
        targetPrefix.normalization_prefix).unrestricted_terminal_normalization_statement :=
  selected_domain_final_closure_component_target_from_obligation_interface
    targetPrefix.final_closure_obligation

/--
Build the four-component prefix from the existing repair-descent interface, the
dependent zero-defect reentry interface, the dependent unrestricted terminal
normalization interface, and the dependent final-closure interface.
-/
def selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_prefix_from_obligation_interfaces
    (repairIface : SelectedDomainRepairDescentObligationInterface)
    (zeroIface :
      SelectedDomainZeroDefectReentryObligationInterface
        repairIface.repair_descent_obligation_statement)
    (normalizationIface :
      SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
        (selected_domain_zero_defect_reentry_component_from_target_prefix
          (selected_domain_repair_descent_zero_defect_reentry_prefix_from_obligation_interfaces
            repairIface
            zeroIface)).zero_defect_selected_domain_reentry_statement)
    (finalIface :
      SelectedDomainFinalClosureObligationInterface
        (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
          (selected_domain_repair_descent_zero_defect_reentry_normalization_prefix_from_obligation_interfaces
            repairIface
            zeroIface
            normalizationIface)).unrestricted_terminal_normalization_statement) :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureTargetPrefix :=
  { normalization_prefix :=
      selected_domain_repair_descent_zero_defect_reentry_normalization_prefix_from_obligation_interfaces
        repairIface
        zeroIface
        normalizationIface
    final_closure_obligation :=
      finalIface }

/--
The final-closure component statement follows from the bounded obligation
interface, assuming the unrestricted terminal-normalization statement required by
the dependent stack.
-/
theorem final_closure_statement_from_obligation_interface
    {unrestricted_terminal_normalization_statement : Prop}
    (iface :
      SelectedDomainFinalClosureObligationInterface
        unrestricted_terminal_normalization_statement)
    (hNormalization : unrestricted_terminal_normalization_statement) :
    (selected_domain_final_closure_component_target_from_obligation_interface
      iface).final_closure_statement :=
  (selected_domain_final_closure_component_target_from_obligation_interface
    iface).final_closure_discharge hNormalization

/--
The final-closure component statement follows from the four-component target
prefix, assuming the prefix unrestricted terminal-normalization statement.

Boundary: this does not refine unrestricted Oblivion closure, does not construct
`defect_atoms`, and does not solve unconditional unrestricted Oblivion Atom
closure.
-/
theorem final_closure_statement_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureTargetPrefix)
    (hNormalization :
      (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
        targetPrefix.normalization_prefix).unrestricted_terminal_normalization_statement) :
    (selected_domain_final_closure_component_from_target_prefix
      targetPrefix).final_closure_statement :=
  (selected_domain_final_closure_component_from_target_prefix
    targetPrefix).final_closure_discharge hNormalization

end Frontier
end Chronos
