from pathlib import Path
lean = Path("lean/Chronos/Frontier/SelectedDomainRepairDescentObligationInterface.lean").read_text()
artifact = Path("artifacts/external_validation/selected_domain_repair_descent_obligation_interface_2026_06_24.json").read_text()
doc = Path("docs/status/SELECTED_DOMAIN_REPAIR_DESCENT_OBLIGATION_INTERFACE_2026_06_24.md").read_text()
assert "SelectedDomainRepairDescentObligationInterface" in lean and "SelectedDomainRepairDescentObligationInterface" in artifact and "SelectedDomainRepairDescentObligationInterface" in doc
assert "SelectedDomainRepairDescentComponentTarget" in lean and "SelectedDomainRepairDescentComponentTarget" in artifact and "SelectedDomainRepairDescentComponentTarget" in doc
assert "selected_domain_repair_descent_component_target_from_obligation_interface" in lean and "selected_domain_repair_descent_component_target_from_obligation_interface" in artifact and "selected_domain_repair_descent_component_target_from_obligation_interface" in doc
assert "repair_descent_component_statement_from_obligation_interface" in lean and "repair_descent_component_statement_from_obligation_interface" in artifact and "repair_descent_component_statement_from_obligation_interface" in doc
assert "repair_descent_obligation_statement_from_interface" in lean and "repair_descent_obligation_statement_from_interface" in artifact and "repair_descent_obligation_statement_from_interface" in doc
assert "repair_descent_obligation_statement" in lean and "repair_descent_obligation_statement" in doc
assert "repair_descent_obligation_discharge" in lean and "repair_descent_obligation_discharge" in doc
assert "SelectedDomainZeroDefectReentryComponentTarget" in artifact
assert "SelectedDomainUnrestrictedTerminalNormalizationComponentTarget" in artifact
assert "SelectedDomainFinalClosureComponentTarget" in artifact
assert "SelectedDomainUnrestrictedOblivionClosureComponentTarget" in artifact
assert "BOUNDARY := not zero_defect_reentry_component_target_refined" in artifact and "BOUNDARY := not zero_defect_reentry_component_target_refined" in doc
assert "BOUNDARY := not unrestricted_terminal_normalization_component_target_refined" in artifact and "BOUNDARY := not unrestricted_terminal_normalization_component_target_refined" in doc
assert "BOUNDARY := not final_closure_component_target_refined" in artifact and "BOUNDARY := not final_closure_component_target_refined" in doc
assert "BOUNDARY := not unrestricted_oblivion_closure_component_target_refined" in artifact and "BOUNDARY := not unrestricted_oblivion_closure_component_target_refined" in doc
assert "BOUNDARY := not defect_atoms_constructed" in artifact and "BOUNDARY := not defect_atoms_constructed" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact and "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "does not construct defect_atoms" in doc
assert "does not solve unconditional unrestricted Oblivion Atom closure" in doc
assert "does not claim construction of the remaining four semantic component targets" in doc
assert "SELECTED_DOMAIN_REPAIR_DESCENT_OBLIGATION_INTERFACE_2026_06_24_OK" in doc
print("SELECTED_DOMAIN_REPAIR_DESCENT_OBLIGATION_INTERFACE_2026_06_24_OK")
