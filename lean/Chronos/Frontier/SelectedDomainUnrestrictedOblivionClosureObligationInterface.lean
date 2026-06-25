import Chronos.Frontier.SelectedDomainFinalClosureObligationInterface

namespace Chronos
namespace Frontier

/--
A bounded obligation interface for exactly one semantic component target:
`SelectedDomainUnrestrictedOblivionClosureComponentTarget`.

The interface is dependent on the final-closure statement, matching the existing
dependent semantic component target stack.
-/
structure SelectedDomainUnrestrictedOblivionClosureObligationInterface
    (final_closure_statement : Prop) : Type where
  unrestricted_oblivion_atom_closure_obligation_statement : Prop
  unrestricted_oblivion_atom_closure_obligation_discharge :
    final_closure_statement →
      unrestricted_oblivion_atom_closure_obligation_statement

/--
Bridge from the bounded unrestricted Oblivion closure obligation interface to
the existing dependent unrestricted Oblivion closure semantic component target.
-/
def selected_domain_unrestricted_oblivion_closure_component_target_from_obligation_interface
    {final_closure_statement : Prop}
    (iface :
      SelectedDomainUnrestrictedOblivionClosureObligationInterface
        final_closure_statement) :
    SelectedDomainUnrestrictedOblivionClosureComponentTarget
      final_closure_statement :=
  { unrestricted_oblivion_atom_closure_statement :=
      iface.unrestricted_oblivion_atom_closure_obligation_statement
    unrestricted_oblivion_atom_closure_discharge :=
      iface.unrestricted_oblivion_atom_closure_obligation_discharge }

/--
A five-component prefix of the existing dependent semantic component target
stack, extending the repair-descent + zero-defect reentry +
terminal-normalization + final-closure prefix by exactly one new target:
unrestricted Oblivion closure.
-/
structure SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix : Type where
  final_closure_prefix :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureTargetPrefix
  unrestricted_oblivion_closure_obligation :
    SelectedDomainUnrestrictedOblivionClosureObligationInterface
      (selected_domain_final_closure_component_from_target_prefix
        final_closure_prefix).final_closure_statement

/--
Bridge the five-component prefix into the existing dependent semantic component
target stack shape by constructing the unrestricted Oblivion closure component
target over the prefix final-closure statement.
-/
def selected_domain_unrestricted_oblivion_closure_component_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix) :
    SelectedDomainUnrestrictedOblivionClosureComponentTarget
      (selected_domain_final_closure_component_from_target_prefix
        targetPrefix.final_closure_prefix).final_closure_statement :=
  selected_domain_unrestricted_oblivion_closure_component_target_from_obligation_interface
    targetPrefix.unrestricted_oblivion_closure_obligation

/--
Build the five-component prefix from the existing repair-descent interface, the
dependent zero-defect reentry interface, the dependent unrestricted terminal
normalization interface, the dependent final-closure interface, and the
dependent unrestricted Oblivion closure interface.
-/
def selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_oblivion_closure_prefix_from_obligation_interfaces
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
            normalizationIface)).unrestricted_terminal_normalization_statement)
    (oblivionIface :
      SelectedDomainUnrestrictedOblivionClosureObligationInterface
        (selected_domain_final_closure_component_from_target_prefix
          (selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_prefix_from_obligation_interfaces
            repairIface
            zeroIface
            normalizationIface
            finalIface)).final_closure_statement) :
    SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix :=
  { final_closure_prefix :=
      selected_domain_repair_descent_zero_defect_reentry_normalization_final_closure_prefix_from_obligation_interfaces
        repairIface
        zeroIface
        normalizationIface
        finalIface
    unrestricted_oblivion_closure_obligation :=
      oblivionIface }

/--
The unrestricted Oblivion closure component statement follows from the bounded
obligation interface, assuming the final-closure statement required by the
dependent stack.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_obligation_interface
    {final_closure_statement : Prop}
    (iface :
      SelectedDomainUnrestrictedOblivionClosureObligationInterface
        final_closure_statement)
    (hFinal : final_closure_statement) :
    (selected_domain_unrestricted_oblivion_closure_component_target_from_obligation_interface
      iface).unrestricted_oblivion_atom_closure_statement :=
  (selected_domain_unrestricted_oblivion_closure_component_target_from_obligation_interface
    iface).unrestricted_oblivion_atom_closure_discharge hFinal

/--
The unrestricted Oblivion closure component statement follows from the
five-component target prefix, assuming the prefix final-closure statement.

Boundary: this does not construct `defect_atoms`, and does not solve
unconditional unrestricted Oblivion Atom closure.
-/
theorem unrestricted_oblivion_atom_closure_statement_from_target_prefix
    (targetPrefix :
      SelectedDomainRepairDescentZeroDefectReentryNormalizationFinalClosureOblivionClosureTargetPrefix)
    (hFinal :
      (selected_domain_final_closure_component_from_target_prefix
        targetPrefix.final_closure_prefix).final_closure_statement) :
    (selected_domain_unrestricted_oblivion_closure_component_from_target_prefix
      targetPrefix).unrestricted_oblivion_atom_closure_statement :=
  (selected_domain_unrestricted_oblivion_closure_component_from_target_prefix
    targetPrefix).unrestricted_oblivion_atom_closure_discharge hFinal

end Frontier
end Chronos
