import Chronos.Frontier.SelectedDomainDefectSemanticComponentTargets

namespace Chronos
namespace Frontier

/--
A bounded obligation interface for exactly one semantic component target:
`SelectedDomainRepairDescentComponentTarget`.

This isolates the repair-descent target into one named obligation statement
and one corresponding discharge.
-/
structure SelectedDomainRepairDescentObligationInterface : Type where
  repair_descent_obligation_statement : Prop
  repair_descent_obligation_discharge :
    repair_descent_obligation_statement

/--
Bridge from the bounded repair-descent obligation interface to the existing
repair-descent semantic component target.
-/
def selected_domain_repair_descent_component_target_from_obligation_interface
    (iface : SelectedDomainRepairDescentObligationInterface) :
    SelectedDomainRepairDescentComponentTarget :=
  { repair_descent_statement :=
      iface.repair_descent_obligation_statement
    repair_descent_discharge :=
      iface.repair_descent_obligation_discharge }

/--
The repair-descent component statement follows from the bounded obligation
interface bridge.
-/
theorem repair_descent_component_statement_from_obligation_interface
    (iface : SelectedDomainRepairDescentObligationInterface) :
    (selected_domain_repair_descent_component_target_from_obligation_interface
      iface).repair_descent_statement :=
  (selected_domain_repair_descent_component_target_from_obligation_interface
    iface).repair_descent_discharge

/--
The repair-descent obligation statement itself is discharged by the bounded
obligation interface.

Boundary: this does not construct the remaining four semantic component
targets, does not construct `defect_atoms`, and does not solve unconditional
unrestricted Oblivion Atom closure.
-/
theorem repair_descent_obligation_statement_from_interface
    (iface : SelectedDomainRepairDescentObligationInterface) :
    iface.repair_descent_obligation_statement :=
  iface.repair_descent_obligation_discharge

end Frontier
end Chronos
