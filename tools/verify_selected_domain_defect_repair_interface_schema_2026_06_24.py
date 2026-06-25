#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/external_validation/selected_domain_defect_repair_interface_schema_2026_06_24.json"
DOC = ROOT / "docs/status/SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24.md"

data = json.loads(ARTIFACT.read_text())
doc = DOC.read_text()

assert data["target"] == "SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24"
assert data["status"] == "repair_interface_schema_recorded_not_constructed"
assert data["context_target"] == "SELECTED_DOMAIN_DEFECT_BASIS"
assert data["missing_interface"]["name"] == "SelectedDomainDefectRepairStep"
assert data["verifier_token"] == "SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24_OK"

fields = {item["field"]: item for item in data["interface_fields"]}

assert fields["source_witness"]["shape"] == "W_unrestricted"
assert fields["target_witness"]["shape"] == "W_unrestricted"
assert fields["repaired_atom"]["shape"] == "SelectedDomainDefect"
assert fields["residual_atoms"]["shape"] == "Finset SelectedDomainDefect"
assert fields["repair_certificate"]["shape"] == "RepairCertificate source_witness target_witness repaired_atom residual_atoms"

assert "source_witness" in doc
assert "target_witness" in doc
assert "repaired_atom" in doc
assert "residual_atoms" in doc
assert "repair_certificate" in doc
assert "RepairCertificate source_witness target_witness repaired_atom residual_atoms" in doc

assert "repair_preserves_unrestricted_admissibility" in data["required_obligations"]
assert "repair_removes_or_accounts_for_repaired_atom" in data["required_obligations"]
assert "repair_does_not_create_untracked_defects" in data["required_obligations"]
assert "repair_is_terminal_normalization_compatible" in data["required_obligations"]
assert "finite_repair_descent_measure_available" in data["required_obligations"]

assert "repair_preserves_unrestricted_admissibility" in doc
assert "repair_removes_or_accounts_for_repaired_atom" in doc
assert "repair_does_not_create_untracked_defects" in doc
assert "repair_is_terminal_normalization_compatible" in doc
assert "finite_repair_descent_measure_available" in doc

assert "BOUNDARY := not SelectedDomainDefectRepairStep_implemented" in doc
assert "BOUNDARY := not RepairCertificate_implemented" in doc
assert "BOUNDARY := not repair_function_constructed" in doc
assert "BOUNDARY := not defect_atoms_constructed" in doc
assert "BOUNDARY := not repair_descent_theorem_proved" in doc
assert "BOUNDARY := not zero_defect_selected_domain_reentry_proved" in doc
assert "BOUNDARY := not unrestricted_terminal_normalization_closed" in doc
assert "BOUNDARY := not final_closure_claim_proved" in doc

assert "SelectedDomainDefectRepairStep implemented in Lean" in doc
assert "RepairCertificate implemented in Lean" in doc
assert "repair function constructed" in doc
assert "defect_atoms" in doc
assert "repair descent theorem proved" in doc
assert "zero-defect selected-domain reentry proved" in doc
assert "unrestricted terminal normalization closed" in doc
assert "final closure claim" in doc

assert "SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24_OK" in doc

print("SELECTED_DOMAIN_DEFECT_REPAIR_INTERFACE_SCHEMA_2026_06_24_OK")
