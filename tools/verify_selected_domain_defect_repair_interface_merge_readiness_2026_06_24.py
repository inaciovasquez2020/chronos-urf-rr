from pathlib import Path
artifact = Path("artifacts/external_validation/selected_domain_defect_repair_interface_merge_readiness_2026_06_24.json").read_text()
doc = Path("docs/status/SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_MERGE_READINESS_2026_06_24.md").read_text()
assert "SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_MERGE_READINESS_2026_06_24_OK" in doc
assert "docs/selected-domain-defect-repair-interface-2026-06-24" in artifact and "docs/selected-domain-defect-repair-interface-2026-06-24" in doc
assert "daf4d0f8" in artifact and "daf4d0f8" in doc
assert "ready_for_review_or_merge_after_validation" in artifact and "ready_for_review_or_merge_after_validation" in doc
assert "MERGE_ACTION_TAKEN := false" in doc
assert '"merge_action_taken": false' in artifact
assert "STOP_AFTER_COMMIT := true" in doc
assert '"stop_after_commit": true' in artifact
assert "This record does not merge the branch." in doc
assert "Do not merge in this command." in doc
assert "SelectedDomainUnconditionalClosureConstructorObligationMatrix" in artifact and "SelectedDomainUnconditionalClosureConstructorObligationMatrix" in doc
assert "selected_domain_unconditional_unrestricted_oblivion_atom_closure_solved_from_obligation_matrix" in artifact and "selected_domain_unconditional_unrestricted_oblivion_atom_closure_solved_from_obligation_matrix" in doc
assert "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in artifact and "selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc
assert "semantic_prefix_constructor_target" in artifact and "semantic_prefix_constructor_target" in doc
assert "defect_atoms_constructor_target" in artifact and "defect_atoms_constructor_target" in doc
assert "constructor-obligation matrix added" in artifact and "constructor-obligation matrix added" in doc
assert "remaining construction split into semantic_prefix_constructor_target and defect_atoms_constructor_target" in artifact and "remaining construction split into semantic_prefix_constructor_target and defect_atoms_constructor_target" in doc
assert "bounded bridge from obligation matrix to selected-domain closure surface verified" in artifact and "bounded bridge from obligation matrix to selected-domain closure surface verified" in doc
assert "unconditional unrestricted Oblivion Atom closure proof" in artifact and "unconditional unrestricted Oblivion Atom closure proof" in doc
assert "unconditional construction of SelectedDomainUnconditionalClosureConstructorObligationMatrix" in artifact and "unconditional construction of SelectedDomainUnconditionalClosureConstructorObligationMatrix" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in artifact and "BOUNDARY := not selected_domain_unconditional_closure_constructor_obligation_matrix_constructed" in doc
assert "BOUNDARY := not selected_domain_unconditional_closure_constructor_target_constructed_without_matrix" in artifact and "BOUNDARY := not selected_domain_unconditional_closure_constructor_target_constructed_without_matrix" in doc
assert "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in artifact and "BOUNDARY := not unconditional_unrestricted_oblivion_atom_closure_solved" in doc
assert "lake build Chronos.Frontier.SelectedDomainUnconditionalClosureConstructorObligationMatrix" in artifact and "lake build Chronos.Frontier.SelectedDomainUnconditionalClosureConstructorObligationMatrix" in doc
assert "lake build Chronos" in artifact and "lake build Chronos" in doc
assert "git diff --check" in artifact and "git diff --check" in doc
assert "3c8ec4a0" in artifact and "3c8ec4a0" in doc
assert "d10d949b" in artifact and "d10d949b" in doc
assert "3d43db21" in artifact and "3d43db21" in doc
assert "65b3906c" in artifact and "65b3906c" in doc
assert "1de76d56" in artifact and "1de76d56" in doc
assert "b9b852a5" in artifact and "b9b852a5" in doc
assert "16592125" in artifact and "16592125" in doc
assert "f0f447bf" in artifact and "f0f447bf" in doc
assert "6555961c" in artifact and "6555961c" in doc
assert "54098552" in artifact and "54098552" in doc
assert "ad3f2b9f" in artifact and "ad3f2b9f" in doc
assert "0ce64e0d" in artifact and "0ce64e0d" in doc
assert "a3dea496" in artifact and "a3dea496" in doc
assert "ed321f47" in artifact and "ed321f47" in doc
assert "281da9a3" in artifact and "281da9a3" in doc
assert "b38c151f" in artifact and "b38c151f" in doc
assert "daf4d0f8" in artifact and "daf4d0f8" in doc
print("SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_MERGE_READINESS_2026_06_24_OK")
