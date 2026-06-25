from pathlib import Path
lean = Path("lean/Chronos/Frontier/SelectedDomainDefectAtomsConstructionTarget.lean").read_text()
artifact = Path("artifacts/external_validation/selected_domain_defect_atoms_construction_target_2026_06_24.json").read_text()
doc = Path("docs/status/SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTION_TARGET_2026_06_24.md").read_text()
schema = Path("artifacts/external_validation/selected_domain_defect_atoms_schema_branch_obligations_2026_06_24.txt").read_text()
assert "SelectedDomainDefectAtomsConstructionTarget" in lean and "SelectedDomainDefectAtomsConstructionTarget" in artifact and "SelectedDomainDefectAtomsConstructionTarget" in doc
assert "defect_atoms_construction_statement" in lean
assert "defect_atoms_construction_discharge" in lean
assert "defect_atoms_construction_statement_from_target" in lean and "defect_atoms_construction_statement_from_target" in artifact and "defect_atoms_construction_statement_from_target" in doc
assert "terminal_cardinality_defect" in schema and "terminal_cardinality_defect" in artifact and "terminal_cardinality_defect" in doc
assert "selected_domain_reentry_defect" in schema and "selected_domain_reentry_defect" in artifact and "selected_domain_reentry_defect" in doc
assert "repair_step_compatibility_defect" in schema and "repair_step_compatibility_defect" in artifact and "repair_step_compatibility_defect" in doc
assert "normalization_transfer_defect" in schema and "normalization_transfer_defect" in artifact and "normalization_transfer_defect" in doc
assert "terminal_cardinality_of_defect_atoms" in lean and "terminal_cardinality_of_defect_atoms" in artifact and "terminal_cardinality_of_defect_atoms" in doc
assert "zero_defects_imply_selected_domain_reentry" in lean and "zero_defects_imply_selected_domain_reentry" in artifact and "zero_defects_imply_selected_domain_reentry" in doc
assert "repair_step_decreases_or_preserves_defect_atoms" in lean and "repair_step_decreases_or_preserves_defect_atoms" in artifact and "repair_step_decreases_or_preserves_defect_atoms" in doc
assert "defect_atoms_transfer_through_terminal_normalization" in lean and "defect_atoms_transfer_through_terminal_normalization" in artifact and "defect_atoms_transfer_through_terminal_normalization" in doc
assert "terminal_cardinality_of_defect_atoms_from_construction_target" in lean and "terminal_cardinality_of_defect_atoms_from_construction_target" in artifact and "terminal_cardinality_of_defect_atoms_from_construction_target" in doc
assert "zero_defects_imply_selected_domain_reentry_from_construction_target" in lean and "zero_defects_imply_selected_domain_reentry_from_construction_target" in artifact and "zero_defects_imply_selected_domain_reentry_from_construction_target" in doc
assert "repair_step_decreases_or_preserves_defect_atoms_from_construction_target" in lean and "repair_step_decreases_or_preserves_defect_atoms_from_construction_target" in artifact and "repair_step_decreases_or_preserves_defect_atoms_from_construction_target" in doc
assert "defect_atoms_transfer_through_terminal_normalization_from_construction_target" in lean and "defect_atoms_transfer_through_terminal_normalization_from_construction_target" in artifact and "defect_atoms_transfer_through_terminal_normalization_from_construction_target" in doc
assert "docs/selected-domain-defect-atom-schema-2026-06-24" in artifact and "docs/selected-domain-defect-atom-schema-2026-06-24" in doc
assert "8bbeca9b" in artifact and "8bbeca9b" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact and "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "does not solve unconditional unrestricted Oblivion Atom closure" in doc
assert "SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTION_TARGET_2026_06_24_OK" in doc
print("SELECTED_DOMAIN_DEFECT_ATOMS_CONSTRUCTION_TARGET_2026_06_24_OK")
