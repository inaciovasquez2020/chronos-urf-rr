# SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24

## Status

`repair_interface_schema_recorded_not_constructed`

This records a repair-interface schema for `SELECTED_DOMAIN_DEFECT_BASIS`.
It does not construct a repair function or prove selected-domain reentry.

## Missing interface

```text
SelectedDomainDefectRepairStep
Purpose: specify the certified repair move needed after defect atoms are counted
but before selected-domain reentry can be claimed.
Interface fields
Field	Shape	Role
source_witness	W_unrestricted	unrestricted witness before repair
target_witness	W_unrestricted	unrestricted witness after repair
repaired_atom	SelectedDomainDefect	defect atom addressed by this repair step
residual_atoms	Finset SelectedDomainDefect	declared remaining defects after repair
repair_certificate	RepairCertificate source_witness target_witness repaired_atom residual_atoms	evidence that the repair step is admissible
Required obligations
repair_preserves_unrestricted_admissibility
repair_removes_or_accounts_for_repaired_atom
repair_does_not_create_untracked_defects
repair_is_terminal_normalization_compatible
finite_repair_descent_measure_available
Boundary
BOUNDARY := not SelectedDomainDefectRepairStep_implemented
BOUNDARY := not RepairCertificate_implemented
BOUNDARY := not repair_function_constructed
BOUNDARY := not defect_atoms_constructed
BOUNDARY := not repair_descent_theorem_proved
BOUNDARY := not zero_defect_selected_domain_reentry_proved
BOUNDARY := not unrestricted_terminal_normalization_closed
BOUNDARY := not final_closure_claim_proved
Not claimed
SelectedDomainDefectRepairStep implemented in Lean
RepairCertificate implemented in Lean
repair function constructed
defect_atoms constructed
repair descent theorem proved
zero-defect selected-domain reentry proved
unrestricted terminal normalization closed
final closure claim
Verifier token
SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24_OK
