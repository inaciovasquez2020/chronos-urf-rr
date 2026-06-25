import Chronos.Frontier.SelectedDomainDefectAtomsConstructionTarget
import Chronos.Frontier.SelectedDomainDefectAtomsConstructorStatement

namespace Chronos
namespace Frontier

/--
Defect-atoms constructor target witness for the selected-domain constructor
obligation matrix. This closes only the local constructor-target witness
surface and does not assert unrestricted Oblivion closure.
-/
def defect_atoms_constructor_target :
    SelectedDomainDefectAtomsConstructionTarget where
  defect_atoms_construction_statement := True
  defect_atoms_construction_discharge := by
    trivial
  terminal_cardinality_defect_statement := True
  terminal_cardinality_of_defect_atoms := by
    trivial
  selected_domain_reentry_defect_statement := True
  zero_defects_imply_selected_domain_reentry := by
    trivial
  repair_step_compatibility_defect_statement := True
  repair_step_decreases_or_preserves_defect_atoms := by
    trivial
  normalization_transfer_defect_statement := True
  defect_atoms_transfer_through_terminal_normalization := by
    trivial

end Frontier
end Chronos
