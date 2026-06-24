import Chronos.Frontier.SelectedDomainZeroDefectReentryObligationInterface

namespace Chronos
namespace Frontier

/--
A bounded obligation interface for exactly one semantic component target:
`SelectedDomainUnrestrictedTerminalNormalizationComponentTarget`.

The interface is dependent on the zero-defect selected-domain reentry statement,
matching the existing dependent semantic component target stack.
-/
structure SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
    (zero_defect_selected_domain_reentry_statement : Prop) : Type where
  unrestricted_terminal_normalization_obligation_statement : Prop
  unrestricted_terminal_normalization_obligation_discharge :
    zero_defect_selected_domain_reentry_statement →
      unrestricted_terminal_normalization_obligation_statement

/--
Bridge from the bounded unrestricted terminal-normalization obligation interface
to the existing dependent unrestricted terminal-normalization semantic component
target.
-/
def selected_domain_unrestricted_terminal_normalization_component_target_from_obligation_interface
    {zero_defect_selected_domain_reentry_statement : Prop}
    (iface :
      SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
        zero_defect_selected_domain_reentry_statement) :
    SelectedDomainUnrestrictedTerminalNormalizationComponentTarget
      zero_defect_selected_domain_reentry_statement :=
  { unrestricted_terminal_normalization_statement :=
      iface.unrestricted_terminal_normalization_obligation_statement
    unrestricted_terminal_normalization_discharge :=
      iface.unrestricted_terminal_normalization_obligation_discharge }

/--
A three-component prefix of the existing dependent semantic component target
stack, extending the repair-descent + zero-defect reentry prefix by exactly one
new target: unrestricted terminal normalization.
-/
structure SelectedDomainRepairDescentZeroDefectReentryNormalizationTargetPrefix : Type where
  zero_defect_reentry_prefix :
    SelectedDomainRepairDescentZeroDefectReentryTargetPrefix
  unrestricted_terminal_normalization_obligation :
    SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
      (selected_domain_zero_defect_reentry_component_from_target_prefix
        zero_defect_reentry_prefix).zero_defect_selected_domain_reentry_statement

/--
Bridge the three-component prefix into the existing dependent semantic component
target stack shape by constructing the unrestricted terminal-normalization
component target over the prefix zero-defect reentry statement.
-/
def selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationTargetPrefix) :
    SelectedDomainUnrestrictedTerminalNormalizationComponentTarget
      (selected_domain_zero_defect_reentry_component_from_target_prefix
        targetPrefix.zero_defect_reentry_prefix).zero_defect_selected_domain_reentry_statement :=
  selected_domain_unrestricted_terminal_normalization_component_target_from_obligation_interface
    targetPrefix.unrestricted_terminal_normalization_obligation

/--
Build the three-component prefix from the existing repair-descent interface, the
dependent zero-defect reentry interface, and the dependent unrestricted
terminal-normalization interface.
-/
def selected_domain_repair_descent_zero_defect_reentry_normalization_prefix_from_obligation_interfaces
    (repairIface : SelectedDomainRepairDescentObligationInterface)
    (zeroIface :
      SelectedDomainZeroDefectReentryObligationInterface
        repairIface.repair_descent_obligation_statement)
    (normalizationIface :
      SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
        (selected_domain_zero_defect_reentry_component_from_target_prefix
          (selected_domain_repair_descent_zero_defect_reentry_prefix_from_obligation_interfaces
            repairIface
            zeroIface)).zero_defect_selected_domain_reentry_statement) :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationTargetPrefix :=
  { zero_defect_reentry_prefix :=
      selected_domain_repair_descent_zero_defect_reentry_prefix_from_obligation_interfaces
        repairIface
        zeroIface
    unrestricted_terminal_normalization_obligation :=
      normalizationIface }

/--
The unrestricted terminal-normalization component statement follows from the
bounded obligation interface, assuming the zero-defect reentry statement
required by the dependent stack.
-/
theorem unrestricted_terminal_normalization_statement_from_obligation_interface
    {zero_defect_selected_domain_reentry_statement : Prop}
    (iface :
      SelectedDomainUnrestrictedTerminalNormalizationObligationInterface
        zero_defect_selected_domain_reentry_statement)
    (hZero : zero_defect_selected_domain_reentry_statement) :
    (selected_domain_unrestricted_terminal_normalization_component_target_from_obligation_interface
      iface).unrestricted_terminal_normalization_statement :=
  (selected_domain_unrestricted_terminal_normalization_component_target_from_obligation_interface
    iface).unrestricted_terminal_normalization_discharge hZero

/--
The unrestricted terminal-normalization component statement follows from the
three-component target prefix, assuming the prefix zero-defect reentry
statement.

Boundary: this does not refine final closure, unrestricted Oblivion closure,
`defect_atoms`, or unconditional unrestricted Oblivion Atom closure.
-/
theorem unrestricted_terminal_normalization_statement_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationTargetPrefix)
    (hZero :
      (selected_domain_zero_defect_reentry_component_from_target_prefix
        targetPrefix.zero_defect_reentry_prefix).zero_defect_selected_domain_reentry_statement) :
    (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
      targetPrefix).unrestricted_terminal_normalization_statement :=
  (selected_domain_unrestricted_terminal_normalization_component_from_target_prefix
    targetPrefix).unrestricted_terminal_normalization_discharge hZero

end Frontier
end Chronos
