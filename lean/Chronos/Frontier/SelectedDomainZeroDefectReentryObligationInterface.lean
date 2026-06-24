import Chronos.Frontier.SelectedDomainRepairDescentObligationInterface

namespace Chronos
namespace Frontier

/--
A bounded obligation interface for exactly one semantic component target:
`SelectedDomainZeroDefectReentryComponentTarget`.

The interface is dependent on the repair-descent statement, matching the
existing dependent semantic component target stack.
-/
structure SelectedDomainZeroDefectReentryObligationInterface
    (repair_descent_statement : Prop) : Type where
  zero_defect_selected_domain_reentry_obligation_statement : Prop
  zero_defect_selected_domain_reentry_obligation_discharge :
    repair_descent_statement →
      zero_defect_selected_domain_reentry_obligation_statement

/--
Bridge from the bounded zero-defect reentry obligation interface to the
existing dependent zero-defect semantic component target.
-/
def selected_domain_zero_defect_reentry_component_target_from_obligation_interface
    {repair_descent_statement : Prop}
    (iface :
      SelectedDomainZeroDefectReentryObligationInterface
        repair_descent_statement) :
    SelectedDomainZeroDefectReentryComponentTarget
      repair_descent_statement :=
  { zero_defect_selected_domain_reentry_statement :=
      iface.zero_defect_selected_domain_reentry_obligation_statement
    zero_defect_selected_domain_reentry_discharge :=
      iface.zero_defect_selected_domain_reentry_obligation_discharge }

/--
A two-component prefix of the existing dependent semantic component target
stack, containing the already-refined repair-descent target and the newly
refined zero-defect reentry obligation interface.
-/
structure SelectedDomainRepairDescentZeroDefectReentryTargetPrefix : Type where
  repair_descent_component :
    SelectedDomainRepairDescentComponentTarget
  zero_defect_reentry_obligation :
    SelectedDomainZeroDefectReentryObligationInterface
      repair_descent_component.repair_descent_statement

/--
Bridge the two-component prefix into the existing dependent semantic component
target stack shape by constructing the zero-defect reentry component target
over the prefix repair-descent statement.
-/
def selected_domain_zero_defect_reentry_component_from_target_prefix
    (targetPrefix : SelectedDomainRepairDescentZeroDefectReentryTargetPrefix) :
    SelectedDomainZeroDefectReentryComponentTarget
      targetPrefix.repair_descent_component.repair_descent_statement :=
  selected_domain_zero_defect_reentry_component_target_from_obligation_interface
    targetPrefix.zero_defect_reentry_obligation

/--
Build the two-component prefix from the repair-descent obligation interface and
the dependent zero-defect reentry obligation interface.
-/
def selected_domain_repair_descent_zero_defect_reentry_prefix_from_obligation_interfaces
    (repairIface : SelectedDomainRepairDescentObligationInterface)
    (zeroIface :
      SelectedDomainZeroDefectReentryObligationInterface
        repairIface.repair_descent_obligation_statement) :
    SelectedDomainRepairDescentZeroDefectReentryTargetPrefix :=
  { repair_descent_component :=
      selected_domain_repair_descent_component_target_from_obligation_interface
        repairIface
    zero_defect_reentry_obligation :=
      zeroIface }

/--
The zero-defect reentry component statement follows from the bounded obligation
interface, assuming the repair-descent statement required by the dependent
stack.
-/
theorem zero_defect_selected_domain_reentry_statement_from_obligation_interface
    {repair_descent_statement : Prop}
    (iface :
      SelectedDomainZeroDefectReentryObligationInterface
        repair_descent_statement)
    (hRepair : repair_descent_statement) :
    (selected_domain_zero_defect_reentry_component_target_from_obligation_interface
      iface).zero_defect_selected_domain_reentry_statement :=
  (selected_domain_zero_defect_reentry_component_target_from_obligation_interface
    iface).zero_defect_selected_domain_reentry_discharge hRepair

/--
The zero-defect reentry component statement follows from the two-component
target prefix, assuming the prefix repair-descent statement.

Boundary: this does not refine terminal normalization, final closure,
unrestricted Oblivion closure, `defect_atoms`, or unconditional unrestricted
Oblivion Atom closure.
-/
theorem zero_defect_selected_domain_reentry_statement_from_target_prefix
    (targetPrefix : SelectedDomainRepairDescentZeroDefectReentryTargetPrefix)
    (hRepair :
      targetPrefix.repair_descent_component.repair_descent_statement) :
    (selected_domain_zero_defect_reentry_component_from_target_prefix
      targetPrefix).zero_defect_selected_domain_reentry_statement :=
  (selected_domain_zero_defect_reentry_component_from_target_prefix
    targetPrefix).zero_defect_selected_domain_reentry_discharge hRepair

end Frontier
end Chronos
